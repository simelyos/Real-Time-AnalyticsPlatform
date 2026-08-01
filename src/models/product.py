from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    name: str
    category: str
    price: float