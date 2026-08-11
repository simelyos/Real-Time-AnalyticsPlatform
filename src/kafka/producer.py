import json

from confluent_kafka import Producer
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

from src.common.logger import configure_logger

import time
import random



class KafkaProducer:

    def __init__(self, bootstrap_servers: str):
        self._producer = Producer({
            "bootstrap.servers": bootstrap_servers,
        })

    def publish(self, topic: str, message: dict) -> None:
        self._producer.produce(
            topic=topic,
            value=json.dumps(message).encode("utf-8"),
        )

        self._producer.flush()


configure_logger()

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






def order_operation(): # order_items are followed by orders creation. 
        customer_ids = [] 
        
        
        id = customer_service._repository.choose_random_customer_id()
        customer_ids.append(id)
        max_order_id = order_service._repository.max_order_id() 

        order_service._generator.generate(customer_ids)
        orders = order_service._repository.get_orders(max_order_id,False)
        products = product_service._repository.select_all_products()
        order_item_service.generate(orders,products)

while True:
    #order_operation()
    interval=random.choice((1,2,3,4,5))
    time.sleep(interval)
    print(interval)