from src.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    table_name = "customers"

    columns = [
        "first_name",
        "last_name",
        "email",
        "country",
        "created_at",
    ]

   