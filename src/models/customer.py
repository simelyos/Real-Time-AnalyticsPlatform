from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Customer:
    first_name: str
    last_name: str
    email: str
    country: str
    created_at: datetime