from pydantic import BaseModel, Field
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ScreeningCreate(BaseModel):
    title: str
    start_time: str
    total_seats: int = Field(..., gt=0, description="Liczba miejsc musi być większa od 0")

class ScreeningResponse(BaseModel):
    id: int
    title: str
    start_time: str
    total_seats: int
    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    screening_id: int
    seat_number: int = Field(..., gt=0)