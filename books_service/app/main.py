from fastapi import FastAPI, HTTPException
from typing import List

from . import models, db
from .rabbitmq_consumer import RabbitMQConsumer

app = FastAPI()

# consumer instance (started on startup)
_consumer = RabbitMQConsumer()


@app.on_event("startup")
def _startup():
	_consumer.start()


@app.on_event("shutdown")
def _shutdown():
	_consumer.stop()


@app.post("/books", response_model=models.BookRead, status_code=201)
def create_book(book: models.BookCreate):
	return db.create_book(book)


@app.get("/books", response_model=List[models.BookRead])
def list_books():
	return db.list_books()


@app.get("/books/{book_id}", response_model=models.BookRead)
def get_book(book_id: int):
	book = db.get_book(book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")
	return book