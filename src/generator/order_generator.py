import random
from faker import Faker
from datetime import datetime
from src.generator.base import BaseGenerator

class OrderGenerator(BaseGenerator):

    ORDER_STATUSES = [
        ("completed", 0.88),
        ("pending", 0.05),
        ("cancelled", 0.04),
        ("returned", 0.03),
    ]

    def __init__(self):
        self.fake = Faker()

    def generate_order_count(self): # This function will generate a random integer. 
        r = random.random()     # Rationale behind this: 50 percent of the customers will buy only one thing, 35 percent will buy between 2 and 5, 12 percent will buy between 6 to 20.
                                # and only 3 percent will buy between 21 to 100.
        if r < 0.50:
            return 1

        if r < 0.85:
            return random.randint(2, 5)

        if r < 0.97:
            return random.randint(6, 20)

        return random.randint(21, 100)



    def generate(self,customer_ids):
        orders = []

        for customer_id in customer_ids:

            order_count = self.generate_order_count(self)

            for _ in range(order_count):

                status = random.choices(
                    [s for s, _ in self.ORDER_STATUSES], weights=[w for _, w in self.ORDER_STATUSES],k=1)[0]

                orders.append({
                    "customer_id": customer_id,
                    "order_date": self.fake.date_time_between(
                        start_date="-2y",
                        end_date="now"
                    ),
                    "status": status
                })

        return orders