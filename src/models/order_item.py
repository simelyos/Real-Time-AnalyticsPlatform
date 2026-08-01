from dataclasses import dataclass


@dataclass(slots=True)
class OrderItem:
    order_id: int
    product_id: int
    quantity: int
    unit_price: float