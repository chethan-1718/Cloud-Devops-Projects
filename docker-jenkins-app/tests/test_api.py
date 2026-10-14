
import time

import requests


BASE_URL = "http://localhost:8080/api"


def test_api_health():
    response = requests.get(f"{BASE_URL}/health", timeout=5)

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_products_endpoint():
    response = requests.get(f"{BASE_URL}/products", timeout=10)

    assert response.status_code == 200

    data = response.json()
    assert "products" in data

    product_names = [
        product["name"] for product in data["products"]
    ]

    assert "Laptop" in product_names
    assert "Keyboard" in product_names
    assert "Mouse" in product_names


def test_redis_health():
    response = requests.get(
        f"{BASE_URL}/redis-health",
        timeout=5,
    )

    assert response.status_code == 200
    assert response.json()["redis"] == "healthy"


def test_product_cache():
    first_response = requests.get(
        f"{BASE_URL}/products",
        timeout=10,
    )
    second_response = requests.get(
        f"{BASE_URL}/products",
        timeout=10,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    # The cache may already contain products from an earlier request.
    assert first_response.headers.get("X-Cache") in {
        "HIT",
        "MISS",
    }

    # The second request should use the populated cache.
    assert second_response.headers.get("X-Cache") == "HIT"


def test_order_rejects_invalid_quantity():
    response = requests.post(
        f"{BASE_URL}/orders",
        params={
            "product_name": "Keyboard",
            "quantity": 0,
        },
        timeout=10,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Quantity must be greater than zero"
    )


def test_order_processing():
    response = requests.post(
        f"{BASE_URL}/orders",
        params={
            "product_name": "Keyboard",
            "quantity": 1,
        },
        timeout=10,
    )

    assert response.status_code == 200

    order = response.json()

    assert order["status"] == "pending"
    assert order["order_id"] > 0
    assert order["task_id"]

    task_id = order["task_id"]
    deadline = time.monotonic() + 20

    while time.monotonic() < deadline:
        status_response = requests.get(
            f"{BASE_URL}/orders/{task_id}",
            timeout=5,
        )

        assert status_response.status_code == 200

        status = status_response.json()["order_status"]

        if status == "processed":
            return

        assert status in {"pending", "processing"}, (
            f"Unexpected order status: {status}"
        )

        time.sleep(1)

    raise AssertionError(
        f"Order {order['order_id']} was not processed within 20 seconds"
    )
