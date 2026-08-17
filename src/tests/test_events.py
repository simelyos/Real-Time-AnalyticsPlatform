from datetime import datetime

from src.kafka.dashboard.metrics import OrderItemMetric


def test_order_item_metric_creation():

    event = OrderItemMetric(
        event_id="event-123",
        order_id=738,
        customer_id=1065,
        product_id=6489,
        quantity=3,
        unit_price=17.21,
        created_at=datetime.fromisoformat(
            "2026-01-15T01:35:48.806468"
        ),
    )

    assert event.event_id == "event-123"
    assert event.order_id == 738
    assert event.customer_id == 1065
    assert event.product_id == 6489
    assert event.quantity == 3
    assert event.unit_price == 17.21