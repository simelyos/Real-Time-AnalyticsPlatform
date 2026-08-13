from collections import Counter, deque
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(slots=True)
class OrderItemMetric:
    event_id: str
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: float
    created_at: datetime

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


class MetricsStore:

    def __init__(self):
        self._events = deque(maxlen=10_000)

        self._orders = set()

        self._product_quantity = Counter()
        self._product_revenue = Counter()

        self._customer_quantity = Counter()
        self._customer_revenue = Counter()

        self._total_revenue = 0.0
        self._total_items = 0

    def add(self, event: OrderItemMetric) -> None:
        self._events.append(event)

        self._orders.add(event.order_id)

        total = event.total_price

        self._product_quantity[event.product_id] += event.quantity
        self._product_revenue[event.product_id] += total

        self._customer_quantity[event.customer_id] += event.quantity
        self._customer_revenue[event.customer_id] += total

        self._total_items += event.quantity
        self._total_revenue += total

    @property
    def total_items(self) -> int:
        return self._total_items

    @property
    def total_orders(self) -> int:
        return len(self._orders)

    @property
    def total_revenue(self) -> float:
        return self._total_revenue

    def recent_events(self, limit: int = 20):
        return list(self._events)[-limit:]

    def top_products(self, limit: int = 10):
        return [
            {
                "product_id": product_id,
                "quantity": quantity,
                "revenue": self._product_revenue[product_id],
            }
            for product_id, quantity
            in self._product_quantity.most_common(limit)
        ]

    def top_customers(self, limit: int = 10):
        return [
            {
                "customer_id": customer_id,
                "quantity": quantity,
                "revenue": self._customer_revenue[customer_id],
            }
            for customer_id, quantity
            in self._customer_quantity.most_common(limit)
        ]

   

    