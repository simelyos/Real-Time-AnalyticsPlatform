import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5433,
        dbname="analytics",
        user="postgres",
        password="postgres",
    )