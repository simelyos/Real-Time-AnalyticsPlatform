from src.kafka.dashboard.reference_data import ReferenceData


def test_get_customer():

    customer1 = {"customer_id":1,
                 "first_name":"Bob"}

    customer2 = {"customer_id":2,
                 "first_name":"Alice"}
    customers= []
    products = []

    reference_data = ReferenceData(
        customers,
        products,
    )

    reference_data._customers.append(customer1)
    reference_data._customers.append(customer2)

    customer = reference_data.get_customer(2)

    assert customer is not None
    assert customer["first_name"] == "Alice"

def test_get_product():

    customers = []
    products = []
    product1 = {
                "product_id": 100,
                "name": "Laptop",
            }
    
    product2 = {
                "product_id": 101,
                "name": "Mouse",
            }

    

    reference_data = ReferenceData(
        customers,
        products,
    )

    reference_data._products.append(product1)
    reference_data._products.append(product2)
    

    product = reference_data.get_product(101)

    assert product is not None
    assert product["name"] == "Mouse"

def test_get_unknown_customer():

    reference_data = ReferenceData(
        [
            {
                "customer_id": 1,
                "first_name": "John",
            }
        ],
        [],
    )

    customer = reference_data.get_customer(999)

    assert customer is None

def test_get_unknown_product():

    reference_data = ReferenceData(
        [],
        [
            {
                "product_id": 100,
                "name": "Laptop",
            }
        ],
    )

    product = reference_data.get_product(999)

    assert product is None