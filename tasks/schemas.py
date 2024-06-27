from pydantic import BaseModel
from datetime import datetime


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    start_date: datetime = None
    end_date: datetime = None
    
    class Config:
        allow_none = True

class CreateStepSchema (BaseModel):
    
    task_id: int
    description: str
    start_date: datetime = None
    end_date: datetime = None
    
    class Config:
        allow_none = True
