from src.warehouse.connection import get_connection


def load_order_items():

    sql = """
        INSERT INTO warehouse.fact_order_item (
            order_item_id,
            order_id,
            customer_key,
            product_key,
            date_key,
            quantity,
            unit_price,
            total_amount
        )
        SELECT
            oi.order_item_id,
            oi.order_id,
            c.customer_key,
            p.product_key,
            d.date_key,
            oi.quantity,
            oi.unit_price,
            oi.quantity * oi.unit_price

        FROM public.order_items oi

        JOIN public.orders o
            ON oi.order_id = o.order_id

        JOIN warehouse.dim_customer c
            ON o.customer_id = c.customer_id

        JOIN warehouse.dim_product p
            ON oi.product_id = p.product_id

        JOIN warehouse.dim_date d
            ON o.order_date::DATE = d.date

        ON CONFLICT (order_item_id) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

        conn.commit()