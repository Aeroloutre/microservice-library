from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Reçu lors de la création
class LoanCreate(BaseModel):
    book_id: int
    borrower: str


# Stocké en base
class Loan(BaseModel):
    id: int
    book_id: int
    borrower: str
    active: bool
    started_at: datetime
    returned_at: Optional[datetime] = None


# Réponse API
class LoanRead(BaseModel):
    id: int
    book_id: int
    borrower: str
    active: bool
    started_at: datetime
    returned_at: Optional[datetime] = None


model_config = ConfigDict(from_attributes=True)