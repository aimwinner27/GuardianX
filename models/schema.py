from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnumSchema(str, Enum):
    student = "student"
    admin = "admin"
    security = "security"
    technician = "technician"

class UserCreate(BaseModel):
    register_or_name: str
    dob: str
    role: RoleEnumSchema

class UserResponse(BaseModel):
    id: int
    register_or_name: str
    role: RoleEnumSchema

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    register_or_name: str
    dob: str

class Token(BaseModel):
    access_token: str
    token_type: str

class GatePassCreate(BaseModel):
    reason: str
    out_time: datetime
    expected_return_time: datetime

class GatePassResponse(BaseModel):
    id: int
    student_id: int
    reason: str
    out_time: datetime
    expected_return_time: datetime
    status: str
    qr_code_path: Optional[str]

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    description: str
    location: str
    # Image skip for simplicity in Pydantic, using FormData in endpoint 

class ReportResponse(BaseModel):
    id: int
    student_id: int
    description: str
    location: str
    priority: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
