from dataclasses import dataclass
from src.models.base import BaseModel

@dataclass(slots=True)
class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float