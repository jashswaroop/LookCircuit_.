from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    
class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: UUID
    is_active: bool = True
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass
