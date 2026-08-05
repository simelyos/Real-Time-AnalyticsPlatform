import logging

logger = logging.getLogger(__name__)

class CustomerGenerationService:

    def __init__(self,customer_generator,customer_repository):

        self._generator = customer_generator
        self._repository = customer_repository

    def generate(self, count: int):

        logger.info("Generating %s customers",count)

        customers = self._generator.generate(count)

        logger.info("Generated %s customers",count)

        self._repository.save_many(customers)

        return customers
    