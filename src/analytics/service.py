class AnalyticsService:

    def __init__(self, repository):
        self.repository = repository

    def get_summary(self):
        data = self.repository.get_summary()

        data["total_revenue"] = float(
            data["total_revenue"]
        )

        data["average_order_value"] = float(
            data["average_order_value"]
        )

        return data

    def get_top_products(self, limit=10):

        products = self.repository.get_top_products(limit)

        for product in products:
            product["revenue"] = float(
                product["revenue"]
            )

        return products

    def get_top_customers(self, limit=10):
        return self.repository.get_top_customers(limit)

    def get_category_sales(self):
        return self.repository.get_category_sales()