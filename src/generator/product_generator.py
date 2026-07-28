from faker import Faker
import random
from base import BaseGenerator

class ProductGenerator(BaseGenerator):

    PRODUCT_CATALOG = {
        "Electronics": [
            ("Apple MacBook Air M3", 1299.99),
            ("Dell XPS 13", 999.99),
            ("Logitech MX Master 3S", 99.99),
            ("Sony WH-1000XM5", 399.99),
            ("Apple AirPods Pro", 249.99),
            ("Samsung Galaxy S25", 999.99),
            ("LG UltraFine Monitor", 499.99),
            ("Mechanical Keyboard", 129.99)
        ],

        "Books": [
            ("Atomic Habits", 18.99),
            ("Clean Code", 42.99),
            ("Designing Data-Intensive Applications", 54.99),
            ("The Pragmatic Programmer", 39.99),
            ("Deep Work", 21.99),
            ("The Phoenix Project", 27.99)
        ],

        "Clothing": [
            ("Nike Air Max 270", 139.99),
            ("Adidas Hoodie", 59.99),
            ("Levi's 501 Jeans", 69.99),
            ("North Face Jacket", 179.99),
            ("Cotton T-Shirt", 24.99)
        ],

        "Home": [
            ("Dyson Vacuum", 549.99),
            ("Ninja Blender", 89.99),
            ("Coffee Maker", 79.99),
            ("Standing Desk", 299.99),
            ("Office Chair", 249.99)
        ],

        "Sports": [
            ("Basketball", 29.99),
            ("Yoga Mat", 35.99),
            ("Adjustable Dumbbells", 299.99),
            ("Tennis Racket", 159.99),
            ("Fitness Tracker", 149.99)
        ],

        "Beauty": [
            ("Face Cleanser", 19.99),
            ("Vitamin C Serum", 34.99),
            ("Hair Dryer", 89.99),
            ("Electric Toothbrush", 69.99),
            ("Skin Moisturizer", 24.99)
        ]
    }

    def __init__(self):
        self.fake = Faker()

    def generate_product_name(self,base_name: str) -> str:
        return f"{base_name} ({self.fake.bothify(text='??-####').upper()})"


    def generate(self,n: int):
        products = []

        for _ in range(n):

            category = random.choice(list(self.PRODUCT_CATALOG.keys()))

            base_name, base_price = random.choice(self.PRODUCT_CATALOG[category]) # Returns a tuple. Category is coming from above. Then the product is randomly selected. First element of 
                                                                            # tuple goes to base_name and price goes to base_price.
            price_variation = random.uniform(-0.10, 0.10)

            price = round(base_price * (1 + price_variation), 2)

            products.append({
                "name": self.generate_product_name(base_name),
                "category": category,
                "price": price
            })

        return products


