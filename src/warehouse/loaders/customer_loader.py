from src.warehouse.connection import get_connection


def load_customers():

    sql = """
        INSERT INTO warehouse.dim_customer (
            customer_id,
            first_name,
            last_name,
            email,
            country,
            created_at
        )
        SELECT
            customer_id,
            first_name,
            last_name,
            email,
            country,
            created_at
        FROM public.customers

        ON CONFLICT (customer_id) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

        conn.commit()