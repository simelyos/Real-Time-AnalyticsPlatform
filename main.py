from  src.common.db import get_connection
from src.generator.factory import GeneratorFactory
from src.ingest.postgres_loader import PostgresLoader




connection = get_connection()
customer_generator = GeneratorFactory.customer()
customers = customer_generator.generate(10)

print(customers)

with PostgresLoader(connection) as loader:

    loader.load_customers(customers)
    
