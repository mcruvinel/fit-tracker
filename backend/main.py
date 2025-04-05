from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List
import os
import json
from pathlib import Path

# Importações locais
from database import get_db, engine
from models import Base, User, Workout
from auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from fit_parser import FITParser
from report_service import PDFReportGenerator

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para requisições/respostas
class UserCreate(BaseModel):
    username: str
    password: str

class WorkoutResponse(BaseModel):
    id: int
    filename: str
    activity_type: str
    start_time: datetime
    duration: float
    distance: float
    calories: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True

# Rota raiz
@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": "Bem-vindo à API de Workouts Garmin"}

# Rota de registro
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    return {"username": new_user.username, "message": "User created successfully"}

# Autenticação
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas protegidas
@app.get("/users/me")
async def read_users_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == current_user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": db_user.username,
        "is_active": db_user.is_active
    }

@app.post("/upload-workout/", response_model=WorkoutResponse)
async def upload_workout(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.fit'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .FIT são aceitos")
    
    try:
        # Processa o arquivo
        contents = await file.read()
        parser = FITParser()
        workout_data = parser.parse(contents)
        
        # Converte datas para datetime (com tratamento de None)
        start_time = datetime.fromisoformat(workout_data['metadata']['start_time']) if 'start_time' in workout_data['metadata'] else None
        end_time = datetime.fromisoformat(workout_data['metadata']['end_time']) if 'end_time' in workout_data['metadata'] else None
        
        # Cria o workout com tratamento de campos opcionais
        workout = Workout(
            user_id=current_user.id,
            filename=file.filename,
            activity_type=workout_data['metadata'].get('sport', 'unknown'),
            start_time=start_time,
            end_time=end_time,
            duration=workout_data['metadata'].get('total_elapsed_time'),
            distance=workout_data['metadata'].get('total_distance'),
            calories=workout_data['metadata'].get('total_calories', 0),
            avg_hr=workout_data['metadata'].get('avg_heart_rate'),
            max_hr=workout_data['metadata'].get('max_heart_rate'),
            avg_speed=workout_data['metadata'].get('avg_speed'),
            max_speed=workout_data['metadata'].get('max_speed'),
            ascent=workout_data['metadata'].get('total_ascent'),
            descent=workout_data['metadata'].get('total_descent'),
            raw_data=json.dumps(workout_data),
            processed=True
        )
        
        db.add(workout)
        db.commit()
        db.refresh(workout)
        return workout
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Arquivo FIT inválido: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@app.get("/workouts/", response_model=List[WorkoutResponse])
async def get_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
    return workouts