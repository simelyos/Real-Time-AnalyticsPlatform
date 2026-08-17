from datetime import datetime

from src.kafka.dashboard.metrics import MetricsStore

from src.kafka.dashboard.metrics import OrderItemMetric


def create_event(
    event_id,
    order_id,
    customer_id,
    product_id,
    quantity,
    unit_price,
):
    return OrderItemMetric(
        event_id=event_id,
        order_id=order_id,
        customer_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        created_at=datetime.now(),
    )


def test_total_orders():

    metrics = MetricsStore()

    metrics.add(
        create_event(
            "event-1",
            100,
            1,
            10,
            2,
            20.0,
        )
    )

    metrics.add(
        create_event(
            "event-2",
            101,
            2,
            11,
            1,
            30.0,
        )
    )

    assert metrics.total_orders == 2

def test_total_items():

    metrics = MetricsStore()

    metrics.add(
        create_event(
            "event-1",
            100,
            1,
            10,
            3,
            20.0,
        )
    )

    metrics.add(
        create_event(
            "event-2",
            101,
            2,
            11,
            5,
            10.0,
        )
    )

    assert metrics.total_items == 8

def test_total_revenue():

    metrics = MetricsStore()

    metrics.add(
        create_event(
            "event-1",
            100,
            1,
            10,
            3,
            20.0,
        )
    )

    metrics.add(
        create_event(
            "event-2",
            101,
            2,
            11,
            2,
            10.0,
        )
    )

    assert metrics.total_revenue == 80.0

def test_recent_events():

    metrics = MetricsStore()

    event = create_event(
        "event-1",
        100,
        1,
        10,
        2,
        25.0,
    )

    metrics.add(event)

    events = metrics.recent_events()

    assert len(events) == 1
    assert events[0].event_id == "event-1"