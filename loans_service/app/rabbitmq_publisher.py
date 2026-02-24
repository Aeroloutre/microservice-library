import os
import json

try:
    import pika
except Exception:  # pragma: no cover - optional dependency at runtime
    pika = None


def publish_book_borrowed(loan) -> bool:
    """Publish a `book.borrowed` event to RabbitMQ. Returns True if published."""
    if pika is None:
        print("pika not installed — skipping RabbitMQ publish")
        return False


def publish_book_returned(loan) -> bool:
    """Publish a `book.returned` event to RabbitMQ. Returns True if published."""
    if pika is None:
        print("pika not installed — skipping RabbitMQ publish")
        return False

    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    params = pika.URLParameters(url)

    body = json.dumps({
        "id": loan.book_id,
        "book_id": loan.book_id,
        "loan_id": loan.id,
        "borrower": loan.borrower,
    })

    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange="events", exchange_type="topic", durable=True)
        ch.basic_publish(
            exchange="events",
            routing_key="book.returned",
            body=body,
            properties=pika.BasicProperties(content_type="application/json"),
        )
        conn.close()
        return True
    except Exception as exc:  # pragma: no cover - runtime network error
        print(f"Failed to publish RabbitMQ message: {exc}")
        return False

    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    params = pika.URLParameters(url)

    body = json.dumps({
        "id": loan.book_id,
        "book_id": loan.book_id,
        "loan_id": loan.id,
        "borrower": loan.borrower,
    })

    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange="events", exchange_type="topic", durable=True)
        ch.basic_publish(
            exchange="events",
            routing_key="book.borrowed",
            body=body,
            properties=pika.BasicProperties(content_type="application/json"),
        )
        conn.close()
        return True
    except Exception as exc:  # pragma: no cover - runtime network error
        print(f"Failed to publish RabbitMQ message: {exc}")
        return False
