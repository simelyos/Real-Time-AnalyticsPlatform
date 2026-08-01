from src.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository):

    table_name = "products"

    columns = [
        "name",
        "category",
        "price",
    ]

    