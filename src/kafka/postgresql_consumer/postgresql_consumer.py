import json
from src.generator.customer_generator import CustomerGenerator
from src.generator.order_generator import OrderGenerator
from src.generator.order_item_generator import OrderItemGenerator
from src.generator.product_generator import ProductGenerator

from src.repositories.customer_repository import CustomerRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.order_item_repository import OrderItemRepository
from src.repositories.product_repository import ProductRepository

from src.services.customer_generation_service import CustomerGenerationService
from src.services.product_generation_service import ProductGenerationService
from src.services.order_generation_service import OrderGenerationService
from src.services.order_item_generation_service import OrderItemGenerationService
from src.common.db import get_connection

from confluent_kafka import Consumer

from src.models.order_item import OrderItem



connection = get_connection()

customer_repository = CustomerRepository(connection)
customer_generator = CustomerGenerator()
customer_service = CustomerGenerationService(customer_generator,customer_repository)

product_repository = ProductRepository(connection)
product_generator = ProductGenerator()
product_service = ProductGenerationService(product_generator,product_repository)

order_repository = OrderRepository(connection)
order_generator = OrderGenerator()
order_service = OrderGenerationService(order_generator,order_repository)

order_item_repository = OrderItemRepository(connection)
order_item_generator = OrderItemGenerator()
order_item_service = OrderItemGenerationService(order_item_generator,order_item_repository)


class OrderItemConsumer:

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str,
        repository: OrderItemRepository,
    ):
        self._consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        })

        self._repository = repository

    def start(self) -> None:
        self._consumer.subscribe(["order-items"])

        try:
            while True:
                message = self._consumer.poll(1.0)
                if message is not None:
                    print(message.value())
                

                if message is None:
                    print(message)  
                    continue

                if message.error():
                    print(f"Kafka error: {message.error()}")
                    continue

                self._process_message(message)

        finally:
            
            self._consumer.close()

        

    def _process_message(self, message) -> None:
        data = json.loads(
            message.value().decode("utf-8")
        )

        order_items = []

        order_item=OrderItem(
            order_id=data["order_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            unit_price=data["unit_price"]
        )

        order_items.append(order_item)

        self._repository.save_many(order_items)

while True:

    order_item_consumer = OrderItemConsumer("localhost:9092","order-item-db-writer",order_item_repository)
    consumer = order_item_consumer._consumer
    message = order_item_consumer.start()

    print(message)