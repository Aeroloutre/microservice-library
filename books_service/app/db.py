from typing import List, Optional

from . import models

_books: List[models.Book] = []
_next_id = 1


def create_book(book_create: models.BookCreate) -> models.Book:
	global _next_id
	book = models.Book(id=_next_id, title=book_create.title, author=book_create.author, available=True)
	_books.append(book)
	_next_id += 1
	return book


def list_books() -> List[models.Book]:
	return _books.copy()


def get_book(book_id: int) -> Optional[models.Book]:
	for b in _books:
		if b.id == book_id:
			return b
	return None


def set_availability(book_id: int, available: bool) -> Optional[models.Book]:
	for i, b in enumerate(_books):
		if b.id == book_id:
			updated = models.Book(id=b.id, title=b.title, author=b.author, available=available)
			_books[i] = updated
			return updated
	return None
