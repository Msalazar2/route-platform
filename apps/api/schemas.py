from pydantic import BaseModel, Field
from datetime import datetime

class NoteCreate(BaseModel):
    body: str = Field(min_length=1)
    author: str | None = None

class NoteOut(BaseModel):
    id: int
    created_at: datetime
    body: str
    author: str | None

    class Config:
        from_attributes = True
