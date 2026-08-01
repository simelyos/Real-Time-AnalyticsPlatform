from faker import Faker
import random

from src.generator.base import BaseGenerator
from src.models.customer import Customer


class CustomerGenerator(BaseGenerator):

    COUNTRIES = [
        "USA",
        "Canada",
        "Germany",
        "Türkiye",
        "Japan",
        "Brazil"
    ]

    def __init__(self):
        self.fake = Faker()

    def generate(self, count: int):

        customers = []

        for _ in range(count):

            customers.append(
                    Customer(
                        first_name=self.fake.first_name(),
                        last_name=self.fake.last_name(),
                        email=self.fake.unique.email(),
                        country=random.choice(self.COUNTRIES),
                        created_at=self.fake.date_time_between(
                        start_date="-2y",
                        end_date="now"
                ),
            )
    )   

        return customers