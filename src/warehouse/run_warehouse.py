from src.warehouse.loaders.customer_loader import load_customers
from src.warehouse.loaders.product_loader import load_products 
from src.warehouse.loaders.order_item_loader import load_order_items


def run():

    print("Loading customers...")
    load_customers()

    print("Loading products...")
    load_products()

    print("Loading order items...")
    load_order_items()

    print("Warehouse load complete.")


if __name__ == "__main__":
    run()