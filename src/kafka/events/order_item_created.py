from dataclasses import dataclass
from datetime import datetime



@dataclass(slots=True)
class OrderItemCreatedEvent:
    event_id: str
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    created_at: datetime
    unit_price: float

    def to_dict(self) -> dict:
        return {
            "event_type": "order_item_created",
            "event_id": str(self.event_id),
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "unit_price": float(self.unit_price)
        }