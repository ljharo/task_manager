from pydantic import BaseModel
from datetime import date


class CreateStepSchema (BaseModel):
    
    task_id: int
    description: str
    start_date: date = None
    end_date: date = None


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    start_date: date = None
    end_date: date = None