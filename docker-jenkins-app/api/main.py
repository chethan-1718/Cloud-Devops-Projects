
import json
import os
from contextlib import asynccontextmanager

import redis
from celery import Celery
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine


# Redis connection
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# Celery client
celery_app = Celery(
    "order_api",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables that do not exist
    Base.metadata.create_all(bind=engine)

    # Safely add task_id to an existing orders table
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE orders "
                "ADD COLUMN IF NOT EXISTS task_id VARCHAR(100)"
            )
        )

    # Insert sample products if the table is empty
    db = SessionLocal()
    try:
        if db.query(models.Product).count() == 0:
            db.add_all([
                models.Product(name="Laptop", price=75000),
                models.Product(name="Keyboard", price=2500),
                models.Product(name="Mouse", price=1200),
            ])
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(lifespan=lifespan)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "E-commerce API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/redis-health")
def redis_health():
    try:
        redis_client.ping()
        return {"redis": "healthy"}
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Redis unavailable"
        ) from exc


@app.get("/products")
def get_products(
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        cached_products = redis_client.get("products")

        if cached_products:
            response.headers["X-Cache"] = "HIT"
            return json.loads(cached_products)

        products = db.query(models.Product).all()

        product_response = {
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price
                }
                for product in products
            ]
        }

        redis_client.setex(
            "products",
            60,
            json.dumps(product_response)
        )

        response.headers["X-Cache"] = "MISS"
        return product_response

    except redis.RedisError:
        # Keep products available even if Redis is unavailable
        products = db.query(models.Product).all()
        response.headers["X-Cache"] = "BYPASS"

        return {
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price
                }
                for product in products
            ]
        }


@app.post("/orders")
def create_order(
    product_name: str,
    quantity: int,
    db: Session = Depends(get_db)
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    product = (
        db.query(models.Product)
        .filter(models.Product.name == product_name)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Save the order first to obtain its database ID
    order = models.Order(
        product_name=product.name,
        quantity=quantity,
        status="pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    try:
        # Queue the task using the real order ID
        task = celery_app.send_task(
            "tasks.process_order",
            args=[order.id, product.name, quantity]
        )

        # Save the Celery task ID
        order.task_id = task.id
        db.commit()
        db.refresh(order)

    except Exception as exc:
        # The order exists even if queue submission fails
        order.status = "failed"
        db.commit()

        raise HTTPException(
            status_code=503,
            detail="Could not queue order for processing"
        ) from exc

    return {
        "message": "Order accepted for processing",
        "order_id": order.id,
        "task_id": order.task_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": order.status
    }


@app.get("/orders/{task_id}")
def get_order_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    order = (
        db.query(models.Order)
        .filter(models.Order.task_id == task_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.id,
        "task_id": order.task_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "order_status": order.status
    }
