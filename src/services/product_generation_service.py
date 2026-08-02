

class ProductGenerationService:

    def __init__(
        self,
        product_generator,
        product_repository,
    ):
        self._generator = product_generator
        self._repository = product_repository

    def generate(self, count: int):

        products = self._generator.generate(count)

        self._repository.save_many(products)

        return products