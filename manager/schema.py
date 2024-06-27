from pydantic import BaseModel

class RegisterLogSchema(BaseModel):
    
    internal_key: str
    address_ip: str
    api_name: str
    method: str


class UpdateLogSchema(BaseModel):

    log_id: int
    status_id: int
    address_ip: str
    internal_key: str 