from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

from models import Workout

class WorkoutComparator:
    @staticmethod
    def compare_workouts(db: Session, workout_ids: List[int]) -> Dict[str, Any]:
        workouts = db.query(Workout).filter(Workout.id.in_(workout_ids)).all()
        
        if len(workouts) < 2:
            raise ValueError("Pelo menos 2 workouts necessários para comparação")
        
        comparison_data = []
        for workout in workouts:
            comparison_data.append({
                'id': workout.id,
                'name': workout.filename,
                'date': workout.start_time,
                'distance': workout.distance,
                'duration': workout.duration,
                'avg_hr': workout.avg_hr,
                'max_hr': workout.max_hr,
                'ascent': workout.ascent,
                'descent': workout.descent
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Análise comparativa
        analysis = {
            'distance_improvement': (df['distance'].iloc[-1] - df['distance'].iloc[0]) / df['distance'].iloc[0] * 100,
            'hr_trend': df['avg_hr'].mean()
        }
        
        return {
            'workouts': comparison_data,
            'analysis': analysis,
            'stats': df.describe().to_dict()
        }

    @staticmethod
    def get_comparable_workouts(db: Session, user_id: int, activity_type: str = None):
        query = db.query(Workout).filter(Workout.user_id == user_id)
        
        if activity_type:
            query = query.filter(Workout.activity_type == activity_type)
            
        return query.order_by(Workout.start_time.desc()).all()