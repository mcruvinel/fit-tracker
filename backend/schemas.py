from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkoutExport(BaseModel):
    id: int
    filename: str
    start_time: str
    activity_type: str
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}