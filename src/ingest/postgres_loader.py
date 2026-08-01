from psycopg import Connection
from psycopg.rows import dict_row


class PostgresLoader:

    def __init__(self, connection: Connection):
        self.connection = connection

    def insert_many(self, table: str, columns: list[str], rows: list[tuple]):

        placeholders = ", ".join(["%s"] * len(columns))

        sql = f"""
            INSERT INTO {table}
            ({", ".join(columns)})
            VALUES ({placeholders}) 
        """


        print(sql)
        print(rows)
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            

        self.connection.commit()

    def load_customers(self, customers):

        rows = [
            (
                c.first_name,
                c.last_name,
                c.email,
                c.country,
                c.created_at
            )
            for c in customers
        ]

        self.insert_many(
            "customers",
            [
                "first_name",
                "last_name",
                "email",
                "country",
                "created_at"
            ],
            rows
        )

    def load_products(self,products):

        rows = [
            (
               p.name,
               p.category,
               p.price

            )
            for p in products
        ]

        self.insert_many("products",["name","category","price"],rows)

    def load_orders(self,orders):

        rows = [
            (
                o.customer_id,
                o.order_date,
                o.status
            )
            for o in orders
        ]

        self.insert_many("orders",["customer_id","order_date","status"],rows)

    def load_order_items(self,order_items):

        rows = [
            (
                od.order_id,
                od.product_id,
                od.quantity,
                od.unit_price
            )
            for od in order_items
        ]

        self.insert_many("order_items",["order_id","product_id","quantity","unit_price"],rows)


    def __enter__(self):
        self.connection = self.connection
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()