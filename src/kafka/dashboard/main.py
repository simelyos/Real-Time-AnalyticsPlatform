import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import asyncio


from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, WebSocketDisconnect

from src.kafka.dashboard.consumer import DashboardConsumer
from src.kafka.dashboard.metrics import MetricsStore


from src.kafka.dashboard.consumer import DashboardConsumer
from src.kafka.dashboard.metrics import MetricsStore

from src.kafka.dashboard.reference_data import ReferenceData

from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository

from src.common.db import get_connection


connection = get_connection()

customer_repository = CustomerRepository(connection)
product_repository = ProductRepository(connection)

metrics = MetricsStore()




def start_kafka_consumer() -> None:
    print("Starting dashboard Kafka consumer...")

    try:
        consumer = DashboardConsumer(
            bootstrap_servers="localhost:9092",
            metrics=metrics,
            
        )   

        consumer.start()

    except Exception as e:
        print(f"Dashboard consumer failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    

    consumer_thread = threading.Thread(
            target=start_kafka_consumer,
            daemon=True,
        )
    consumer_thread.start()

    yield




app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="src/kafka/dashboard/static"),
    name="static",
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json({
                "total_orders": metrics.total_orders,
                "total_items": metrics.total_items,
                "total_revenue": metrics.total_revenue,
                "top_products": metrics.top_products(),
                "top_customers": metrics.top_customers(),
                "recent_events": [
                    {
                        "event_id": event.event_id,
                        "order_id": event.order_id,
                        "customer_id": event.customer_id,
                        "product_id": event.product_id,
                        "quantity": event.quantity,
                        "unit_price": event.unit_price,
                        "total_price": event.total_price,
                        "created_at": event.created_at.isoformat(),
                    }
                    for event in metrics.recent_events()
                ],
            })

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Dashboard client disconnected")


@app.get("/")
def dashboard():
    return FileResponse(
        "src/kafka/dashboard/static/index.html"
    )


@app.get("/metrics")
def get_metrics():
    return {
        "total_orders": metrics.total_orders,   
        "total_items": metrics.total_items,
        "total_revenue": metrics.total_revenue,
        "top_products": metrics.top_products(),
        "top_customers": metrics.top_customers(),
    }

@app.get("/recent")
def get_recent_events(request: Request):

    reference_data = ReferenceData(customer_repository,product_repository)
    reference_data.load()
    result = []

    events = metrics.recent_events()

    for event in events:
        print("PROCESSING EVENT:", event)

        product = reference_data.get_product(event.product_id)
        customer = reference_data.get_customer(event.customer_id)

        print("PRODUCT:", product)
        print("CUSTOMER:", customer)

        result.append({
            "event_id": event.event_id,
            "order_id": event.order_id,
            "customer": customer["first_name"] if customer else "Unknown",
            "product": product["name"] if product else "Unknown",
            "quantity": event.quantity,
            "unit_price": event.unit_price,
            "total_price": event.total_price,
            "created_at": event.created_at.isoformat(),
        })

    return result

