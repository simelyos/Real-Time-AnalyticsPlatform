from dataclasses import dataclass
from src.models.base import BaseModel

@dataclass(slots=True)
class Product(BaseModel):
    name: str
    category: str
    price: float


