from src.repositories.base_repository import BaseRepository
from psycopg import Connection
from psycopg import sql
import random



class CustomerRepository(BaseRepository):

    table_name = "customers"

    columns = [
        "first_name",
        "last_name",
        "email",
        "country",
        "created_at",
    ]

    def choose_random_customer_id(self):

        random_id = sql.SQL("""
                    SELECT customer_id FROM customers ORDER BY RANDOM() limit 1
                    """)
        
        with self.connection.cursor() as cursor:
          cursor_result=cursor.execute(random_id)
          id_dict = cursor_result.fetchone()

        returned_id = id_dict["customer_id"]
       
        self.connection.commit()

        return returned_id


        
