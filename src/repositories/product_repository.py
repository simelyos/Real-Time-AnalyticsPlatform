from src.repositories.base_repository import BaseRepository
from psycopg import Connection
from psycopg import sql


class ProductRepository(BaseRepository):

    table_name = "products"

    columns = [
        "name",
        "category",
        "price",
    ]

    def select_all_products(self):

        query = sql.SQL("""
        SELECT * FROM products
        """)


        with self.connection.cursor() as cursor:
            cursor_result=cursor.execute(query)
            products_list = cursor_result.fetchall()

        
        returned_products_list = products_list
        
        self.connection.commit()

        return returned_products_list
        