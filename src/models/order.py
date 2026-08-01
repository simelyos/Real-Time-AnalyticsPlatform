from dataclasses import dataclass
from datetime import datetime
from src.models.base import BaseModel

@dataclass(slots=True)
class Order(BaseModel):
    customer_id: int
    order_date: datetime
    status: str