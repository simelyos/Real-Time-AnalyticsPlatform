from src.repositories.base_repository import BaseRepository
from psycopg import Connection
from psycopg import sql


class OrderRepository(BaseRepository):

    table_name = "orders"

    columns = [
        "customer_id",
        "order_date",
        "status",
    ]


    def get_orders(self,max_order_id,first_creation):
        if first_creation:
             query = sql.SQL("""SELECT * FROM orders""")
        else:
            query = sql.SQL("""SELECT * FROM orders WHERE order_id > {max_id}""".format(max_id=max_order_id))

        with self.connection.cursor() as cursor:
              returned_orders=cursor.execute(query)
              stored_orders = returned_orders.fetchall()

        return stored_orders

    def max_order_id(self):
         query = sql.SQL("""SELECT max(order_id)  FROM orders""")

         with self.connection.cursor() as cursor:
            max_order_id = cursor.execute(query)
            store_max_order_id = max_order_id.fetchone()

         self.connection.commit()

         return store_max_order_id['max']