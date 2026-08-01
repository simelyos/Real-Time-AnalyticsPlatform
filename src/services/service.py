from src.common.db import get_connection
from src.generator.factory import GeneratorFactory
from src.repositories.customer_repository import CustomerRepository
from src.repositories.order_item_repository import OrderItemRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository

connection = get_connection()
customer_generator = GeneratorFactory.customer()
customers = customer_generator.generate(10)

CustomerRepository(connection=connection).save_many(customers)
    
