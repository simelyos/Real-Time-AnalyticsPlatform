class OrderItemGenerationService:
    def __init__(self,order_item_generator,order_item_repository):

        self._generator = order_item_generator
        self._repository = order_item_repository

    def generate(self):
    
            orders= ...
            products= ...


            order_items = self._generator.generate(orders,products)
    
            self._repository.save_many(order_items)
    
            return orders