from  common.db import get_connection
from generator.factory import GeneratorFactory
from ingest.postgres_loader import PostgresLoader

connection = get_connection()
customer_generator = GeneratorFactory.customer()
customers = customer_generator.generate(1)

with PostgresLoader(connection) as loader:

    loader.load_customers(customers)

