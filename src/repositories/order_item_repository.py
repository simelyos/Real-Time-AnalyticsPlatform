from src.repositories.base_repository import BaseRepository

class OrderItemRepository(BaseRepository):

    table_name = "order_items"

    columns = [
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
    ]

   