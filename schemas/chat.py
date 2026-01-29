from pydantic import BaseModel

class ChatCreate(BaseModel):
    name: str
    owner_id: int

class ChatRead(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True