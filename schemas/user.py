from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str
    username: str
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True