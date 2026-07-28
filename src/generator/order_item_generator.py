import random
from base import BaseGenerator


class OrderItemGenerator(BaseGenerator):


    def __init__(self):
        pass

    def generate_item_count(self):

        r = random.random()

        if r < 0.60:
            return 1

        if r < 0.85:
            return 2

        if r < 0.95:
            return 3

        if r < 0.99:
            return 4

        return 5


    def generate_quantity(self,category):

        if category == "Books":
            return random.randint(1, 3)

        if category == "Beauty":
            return random.randint(1, 4)

        return 1



    def generate(self,orders, products):

        items = []

        for order in orders:

            item_count = self.generate_item_count(self)

            first_product = random.choice(products)

            selected_products = [first_product]

            same_category = [# Loop through all the categories and compare the first product's category with other products. If categories are the same and id's are different 
                            # (if they're not the same product) take the products. We're doing this because customers most likely to buy from same categories.
                p for p in products
                if p["category"] == first_product["category"]
                and p["product_id"] != first_product["product_id"]
            ]

            while (
                len(selected_products) < item_count
                and same_category # Until the selected_products have enough items or the products in the same category is finished loop through.
            ):
                product = random.choice(same_category)

                same_category.remove(product)

                selected_products.append(product)

            for product in selected_products:

                items.append({

                    "order_id": order["order_id"],

                    "product_id": product["product_id"],

                    "quantity": self.generate_quantity(
                        product["category"]
                    ),

                    "unit_price": product["price"]
                })

        return items