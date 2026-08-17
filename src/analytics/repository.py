from decimal import Decimal


class AnalyticsRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_summary(self):

        query = """
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                COALESCE(SUM(quantity), 0) AS total_items,
                COALESCE(
                    SUM(quantity * unit_price),
                    0
                ) AS total_revenue
            FROM warehouse.fact_order_item;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        total_orders = row["total_orders"]
        total_items = row["total_items"]
        total_revenue = row["total_revenue"]

        average_order_value = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        return {
            "total_orders": total_orders,
            "total_items": total_items,
            "total_revenue": float(total_revenue),
            "average_order_value": float(average_order_value),
        }

    def get_top_products(self, limit=10):

        query = """
            SELECT
                p.product_id,
                p.name,
                SUM(f.quantity) AS quantity,
                SUM(
                    f.quantity * f.unit_price
                ) AS revenue
            FROM warehouse.fact_order_item f
            JOIN warehouse.dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.product_id,
                p.name
            ORDER BY
                revenue DESC
            LIMIT %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit,))

            rows = cursor.fetchall()

        return [
            {
                "product_id": row["product_id"],
                "name": row["name"],
                "quantity": row["quantity"],
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ]

    def get_top_customers(self, limit=10):
        query = """
            SELECT
                c.customer_id,
                c.first_name,
                c.last_name,
                COUNT(DISTINCT f.order_id) AS orders,
                SUM(f.total_amount) AS spending
            FROM warehouse.fact_order_item f
            JOIN warehouse.dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY
                c.customer_id,
                c.first_name,
                c.last_name
            ORDER BY
                spending DESC
            LIMIT %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

        return [
            {
                "customer_id": row["customer_id"],
                "name": f"{row["first_name"]} {row["last_name"]}",
                "orders": row["orders"],
                "spending": Decimal(row["spending"]),
            }
            for row in rows
        ]

    def get_category_sales(self):
        query = """
            SELECT
                p.category,
                SUM(f.quantity) AS quantity,
                SUM(f.total_amount) AS revenue
            FROM warehouse.fact_order_item f
            JOIN warehouse.dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.category
            ORDER BY
                revenue DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            {
                "category": row["category"],
                "quantity": row["quantity"],
                "revenue": Decimal(row["revenue"]),
            }
            for row in rows
        ]