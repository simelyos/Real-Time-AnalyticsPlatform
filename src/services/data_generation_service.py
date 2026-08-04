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



class DataGenerationService:

    def __init__(
        self,
        customer_service,
        product_service,
        order_service,
        order_item_service,
    ):
        self._customer_service = customer_service
        self._product_service = product_service
        self._order_service = order_service
        self._order_item_service = order_item_service
        


    def generate(self):

        #self._customer_service.generate(1000)

        #self._product_service.generate(2000)

        customer_ids = [] # Choosing customers to create orders.

        for _ in range(10):
            id = self._customer_service._repository.choose_random_customer_id()
            customer_ids.append(id)

        first_time_allocation = False

        if first_time_allocation:
            max_order_id = None
        else:
            max_order_id = self._order_service._repository.max_order_id()

        
        
        self._order_service.generate(customer_ids)

        orders = self._order_service._repository.get_orders(max_order_id,first_time_allocation)

        products = self._product_service._repository.select_all_products()

        self._order_item_service.generate(orders,products)

    


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

data_generation = DataGenerationService(customer_service,product_service,order_service,order_item_service)

data_generation.generate()



