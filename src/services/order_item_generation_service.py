import logging

logger = logging.getLogger(__name__)

class OrderItemGenerationService:
    def __init__(self,order_item_generator,order_item_repository):

        self._generator = order_item_generator
        self._repository = order_item_repository

    def generate(self,orders,products):

            print(orders)
            logger.info("Generating order items for these orders : %s",orders)

            order_items = self._generator.generate(orders,products)


            logger.info("Generated order items for these orders : %s",orders)

            self._repository.save_many(order_items)
    
            return order_items