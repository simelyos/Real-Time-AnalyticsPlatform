# dashboard/consumer.py
import asyncio
import json
import logging
from datetime import datetime

from confluent_kafka import Consumer

from src.kafka.dashboard.metrics import MetricsStore, OrderItemMetric


logger = logging.getLogger(__name__)


class DashboardConsumer:

    def __init__(
        self,
        bootstrap_servers: str,
        metrics: MetricsStore,
        
    ):
        self._consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": "dashboard",
            "auto.offset.reset": "earliest",
        })

        self._metrics = metrics

    def start(self) -> None:

        '''
        Pretty common with other subscribers. Uses a topic name to subscribe to stream inside the Kafka broker
        At the end there is process part.
        '''
        self._consumer.subscribe(["order-items"])

        logger.info("Dashboard consumer started")

        try:
            while True:
                message = self._consumer.poll(1.0)

                if message is None:
                    continue

                if message.error():
                    logger.error(
                        "Kafka error: %s",
                        message.error(),
                    )
                    continue

                self._process(message)

        except KeyboardInterrupt:
            logger.info("Dashboard consumer stopping")

        finally:
            self._consumer.close()

    def _process(self, message) -> None:

        '''
        I have created a class called metrics. This metrics class has an array of OrderItemMetrics.
        The data will be turned to this OrderItemMetric model and then will be appended to the list 
        which is in MetricsStore class.
        '''

        data = json.loads(
            message.value().decode("utf-8")
        )

        

        event = OrderItemMetric(
            event_id=data["event_id"],
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            created_at=datetime.fromisoformat(
                data["created_at"]
            ),
        )

        

        self._metrics.add(event)

        

        