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

import random
import time

from src.common.logger import configure_logger

import uuid

import json

from confluent_kafka import Producer

from src.kafka.events.order_item_created import OrderItemCreatedEvent


class OrderItemProducer:

    def __init__(self, bootstrap_servers: str):
        self._producer = Producer({
            "bootstrap.servers": bootstrap_servers,
        })

    def publish(self, event: OrderItemCreatedEvent) -> None:
        self._producer.produce(
            topic="order-items",
            value=json.dumps(event.to_dict()).encode("utf-8"),
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



def order_operation():

        '''
            A customer id is selected randomly from the database. Then max_order_id is taken from the database. 
            This way, no order_item will be created for the previous records. Then orders are created and stored in the database
            for the selected customer. Then starting from max_order_id orders are selected from the database.
            Then all products are selected. Then orders and products are given to order_item creation. Then order_items are 
            generated. Then they will be converted to JSON and a new model will be created from the values.
        ''' 
        customer_ids = [] 
        
        id = customer_service._repository.choose_random_customer_id()
        customer_ids.append(id)
        max_order_id = order_service._repository.max_order_id() 

        order_service.generate(customer_ids)
        orders = order_service._repository.get_orders(max_order_id,False)
        products = product_service._repository.select_all_products()
        order_items=order_item_service._generator.generate(orders,products)


        for order in orders:
            
            print(order)
            items_to_be_published = []
            for order_item in order_items:
                order_item = order_item.to_dict()
                event_id = uuid.uuid4()
                item=OrderItemCreatedEvent(event_id,order_item["order_id"],customer_ids[0],order_item["product_id"],order_item["quantity"],order["order_date"],order_item["unit_price"])
                items_to_be_published.append(item)
            
        print(items_to_be_published)    


        return items_to_be_published

while True:
    items_to_be_published = order_operation()
    print(items_to_be_published)
    producer = OrderItemProducer("localhost:9092")
    for item in items_to_be_published:
        producer.publish(item)

    wait = random.choice((1,2,3,4,5))
    time.sleep(wait)

