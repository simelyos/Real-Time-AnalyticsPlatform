from src.warehouse.connection import get_connection


def load_products():

    sql = """
        INSERT INTO warehouse.dim_product (
            product_id,
            name,
            category,
            price
        )
        SELECT
            product_id,
            name,
            category,
            price
        FROM public.products

        ON CONFLICT (product_id) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

        conn.commit()