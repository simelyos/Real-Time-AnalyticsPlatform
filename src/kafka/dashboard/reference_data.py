import logging

from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository


logger = logging.getLogger(__name__)


class ReferenceData:

    '''
    This class is for like In-Python caching. Instead of querying everytime order_item comes in
    I have queried the products and customers once and store them here. 
    '''

    def __init__(
        self,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ):
        self._customer_repository = customer_repository
        self._product_repository = product_repository

        self._customers = []
        self._products = []

    def load(self) -> None:
        self._load_customers()
        self._load_products()

        logger.info(
            "Loaded %d customers and %d products",
            len(self._customers),
            len(self._products),
        )

    def _load_customers(self) -> None:
        customers = self._customer_repository.select_all_customers()
        
        self._customers = customers

    def _load_products(self) -> None:
        products = self._product_repository.select_all_products()

        self._products = products

    def get_customer(self, customer_id: int):
        for customer in self._customers:
            if customer["customer_id"] == customer_id:
                return customer
            
        return None

    def get_product(self, product_id: int):
        for product in self._products:
            if product["product_id"] == product_id:
                return product
        
        return None