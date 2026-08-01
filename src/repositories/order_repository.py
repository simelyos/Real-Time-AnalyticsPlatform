from src.repositories.base_repository import BaseRepository

class OrderRepository(BaseRepository):

    table_name = "orders"

    columns = [
        "customer_id",
        "order_date",
        "status",
    ]

   