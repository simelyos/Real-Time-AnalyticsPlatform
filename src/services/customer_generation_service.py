

class CustomerGenerationService:

    def __init__(self,customer_generator,customer_repository):

        self._generator = customer_generator
        self._repository = customer_repository

    def generate(self, count: int):

        customers = self._generator.generate(count)

        self._repository.save_many(customers)

        return customers
    