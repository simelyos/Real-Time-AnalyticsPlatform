import logging

logger = logging.getLogger(__name__)

class ProductGenerationService:

    def __init__(
        self,
        product_generator,
        product_repository,
    ):
        self._generator = product_generator
        self._repository = product_repository

    def generate(self, count: int):

        logger.info("Generating %s products",count)
        
        products = self._generator.generate(count)

        logger.info("Generated %s products.",count)

        self._repository.save_many(products)

        return products