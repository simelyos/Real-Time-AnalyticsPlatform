class OrderGenerationService:

    def __init__(self,order_generator,order_repository):

        self._generator = order_generator
        self._repository = order_repository

    def generate(self,customer_ids):

         
        orders = self._generator.generate(customer_ids)

        self._repository.save_many(orders)

        return orders