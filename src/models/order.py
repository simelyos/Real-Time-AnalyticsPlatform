from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Order:
    customer_id: int
    order_date: datetime
    status: str