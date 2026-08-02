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

        #self._customer_service.generate(10)

        #self._product_service.generate(100)

        customer_ids = []

        for _ in range(10):
            id = self._customer_service._repository.choose_random_customer_id()
            print(id)
            customer_ids.append(id)
        print(customer_ids)
        self._order_service.generate(customer_ids)

        #self._order_item_service.generate()




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


data_generation = DataGenerationService(customer_service,product_service,order_service,...)

data_generation.generate()



