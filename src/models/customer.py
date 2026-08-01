from dataclasses import dataclass
from datetime import datetime
from src.models.base import BaseModel

@dataclass(slots=True)
class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str
    created_at: datetime