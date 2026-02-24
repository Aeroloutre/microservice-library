import os
import json
import threading
from typing import Optional

try:
    import pika
except Exception:  # pragma: no cover - optional runtime dependency
    pika = None

from . import db


class RabbitMQConsumer:
    def __init__(self) -> None:
        self._thread: Optional[threading.Thread] = None
        self._connection = None
        self._stop_event = threading.Event()

    def _on_message(self, ch, method, properties, body):
        try:
            payload = json.loads(body)
            book_id = int(payload.get("id") or payload.get("book_id"))
        except Exception:
            print("Invalid message payload for book event:", body)
            return

        routing = getattr(method, "routing_key", None)
        if routing == "book.borrowed":
            updated = db.set_availability(book_id, False)
            if updated:
                print(f"Marked book {book_id} as borrowed")
            else:
                print(f"Received borrow event for unknown book {book_id}")
        elif routing == "book.returned":
            updated = db.set_availability(book_id, True)
            if updated:
                print(f"Marked book {book_id} as returned (available)")
            else:
                print(f"Received return event for unknown book {book_id}")
        else:
            print("Unhandled routing key", routing)

    def _run(self) -> None:
        if pika is None:
            print("pika not installed — RabbitMQ consumer disabled")
            return

        url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        params = pika.URLParameters(url)

        try:
            self._connection = pika.BlockingConnection(params)
            ch = self._connection.channel()
            ch.exchange_declare(exchange="events", exchange_type="topic", durable=True)
            q = ch.queue_declare(queue='', exclusive=True)
            queue_name = q.method.queue
            # bind to both borrowed and returned events
            ch.queue_bind(exchange="events", queue=queue_name, routing_key="book.borrowed")
            ch.queue_bind(exchange="events", queue=queue_name, routing_key="book.returned")
            ch.basic_consume(queue=queue_name, on_message_callback=self._on_message, auto_ack=True)
            ch.start_consuming()
        except Exception as exc:
            print(f"RabbitMQ consumer stopped: {exc}")

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        try:
            if self._connection:
                self._connection.close()
        except Exception:
            pass
        if self._thread:
            self._thread.join(timeout=1.0)
