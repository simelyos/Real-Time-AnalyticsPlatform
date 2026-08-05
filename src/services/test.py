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

import argparse

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


def get_args():
    parser = argparse.ArgumentParser(description="CLI for Ddata Generation",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c','--customer',type=int,help="Generate customers and write them to customer table.")
    parser.add_argument('-p','--product',type=int,help="Generate products and write them to product table.")
    parser.add_argument('-o','--order',type=int,help="Generate orders and write them to orders table.")
    parser.add_argument('-f','--first-generation',action='store_true',help="Use this option if the database is newly initialized.")



    return parser.parse_args()


args = get_args()

customer_count = args.customer
first_time = args.first_generation
product_count = args.product
order_count = args.order # This number will be provided to order. It will choose random customer_ids. Not very efficient by the way. Refactor, maybe?

def customer_operation():
    if customer_count != None:
        customer_service.generate(customer_count)

def product_operation():
    if product_count != None:
        product_service.generate(product_count)

def order_operation(): # order_items are followed by orders creation. 
    if order_count != None:
        customer_ids = [] 
        
        for _ in range(order_count):
            id = customer_service._repository.choose_random_customer_id()
            customer_ids.append(id)

        if first_time:
            max_order_id = None
        else:
            max_order_id = order_service._repository.max_order_id() 

        order_service.generate(customer_ids)
        orders = order_service._repository.get_orders(max_order_id,first_time)
        products = product_service._repository.select_all_products()
        order_item_service.generate(orders,products)

customer_operation()
order_operation()
product_operation()