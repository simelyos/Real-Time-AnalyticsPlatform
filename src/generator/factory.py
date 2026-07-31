from src.generator.customer_generator import CustomerGenerator
from src.generator.product_generator import ProductGenerator
from src.generator.order_generator import OrderGenerator
from src.generator.order_item_generator import OrderItemGenerator


class GeneratorFactory:


    '''
    With static methods you don't have to instatiate objects to use the classes. You can directly use methods 
    For example think you do GeneratorFactory.customer(). It will return CustomerGenerator. Which can be used with the common method to
    all which is generate(). It can be seen in the main.py.  
    '''

    @staticmethod 
    def customer():
        return CustomerGenerator()

    @staticmethod
    def product():
        return ProductGenerator()

    @staticmethod
    def order():
        return OrderGenerator()

    @staticmethod
    def order_item():
        return OrderItemGenerator()