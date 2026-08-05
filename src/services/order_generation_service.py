import logging

logger = logging.getLogger(__name__)

class OrderGenerationService:

    def __init__(self,order_generator,order_repository):

        self._generator = order_generator
        self._repository = order_repository

    def generate(self,customer_ids):

        logger.info("Generating orders for these customers %s.",customer_ids)

        orders = self._generator.generate(customer_ids)

        logger.info("Generated orders for these customers %s",customer_ids)
        
        self._repository.save_many(orders)

        return orders