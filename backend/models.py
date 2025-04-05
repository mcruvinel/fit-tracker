from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Modelo SQLAlchemy para User
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

# Modelo SQLAlchemy para Workout
class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String(255))
    activity_type = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)  # Adicione nullable=True
    duration = Column(Float)
    distance = Column(Float)
    calories = Column(Integer)
    avg_hr = Column(Integer)
    max_hr = Column(Integer)
    avg_speed = Column(Float, nullable=True)  # Permite valores nulos
    max_speed = Column(Float, nullable=True)
    ascent = Column(Integer, nullable=True)
    descent = Column(Integer, nullable=True)
    raw_data = Column(JSON)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

# Schemas Pydantic
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class WorkoutBase(BaseModel):
    activity_type: str
    start_time: datetime
    end_time: datetime
    duration: float = Field(..., gt=0)
    distance: float = Field(..., ge=0)

class WorkoutCreate(WorkoutBase):
    filename: str
    user_id: int = Field(..., gt=0)

class WorkoutResponse(WorkoutBase):
    id: int
    calories: Optional[int] = None
    processed: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}