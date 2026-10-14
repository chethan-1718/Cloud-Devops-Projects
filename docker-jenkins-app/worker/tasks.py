
import os
import time

from celery import Celery
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

celery_app = Celery(
    "order_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@celery_app.task
def process_order(
    order_id: int,
    product_name: str,
    quantity: int
):
    db = SessionLocal()

    try:
        # Mark order as processing
        db.execute(
            text(
                "UPDATE orders SET status = 'processing' "
                "WHERE id = :order_id"
            ),
            {"order_id": order_id}
        )
        db.commit()

        print(f"Processing order {order_id}...")
        time.sleep(5)

        # Mark order as processed
        db.execute(
            text(
                "UPDATE orders SET status = 'processed' "
                "WHERE id = :order_id"
            ),
            {"order_id": order_id}
        )
        db.commit()

        print(
            f"Order {order_id} processed: "
            f"{quantity} x {product_name}"
        )

        return {
            "order_id": order_id,
            "status": "processed",
            "product": product_name,
            "quantity": quantity
        }

    except Exception:
        db.rollback()

        try:
            db.execute(
                text(
                    "UPDATE orders SET status = 'failed' "
                    "WHERE id = :order_id"
                ),
                {"order_id": order_id}
            )
            db.commit()
        except Exception:
            db.rollback()

        raise

    finally:
        db.close()
