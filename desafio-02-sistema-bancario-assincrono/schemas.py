from pydantic import BaseModel, Field
from datetime import datetime
from models import TransactionType

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionCreate(BaseModel):
    type: TransactionType
    # Garante que o valor inserido seja estritamente maior que zero
    amount: float = Field(..., gt=0, description="O valor deve ser maior que zero.")

class TransactionResponse(BaseModel):
    id: int
    type: TransactionType
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True

class StatementResponse(BaseModel):
    balance: float
    transactions: list[TransactionResponse]
