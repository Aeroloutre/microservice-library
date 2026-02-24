from fastapi import FastAPI, HTTPException
from typing import List

from . import models, db
from . import rabbitmq_publisher

app = FastAPI()


@app.post("/loans", response_model=models.LoanRead, status_code=201)
def create_loan(loan: models.LoanCreate):
	created = db.create_loan(loan)
	published = rabbitmq_publisher.publish_book_borrowed(created)
	if not published:
		# log but still return success for now
		print("Warning: failed to publish book.borrowed event")
	return created


@app.get("/loans", response_model=List[models.LoanRead])
def list_loans():
	return db.list_loans()


@app.post("/loans/{loan_id}/return", response_model=models.LoanRead)
def return_loan(loan_id: int):
	loan = db.close_loan(loan_id)
	if not loan:
		raise HTTPException(status_code=404, detail="Loan not found")
	published = rabbitmq_publisher.publish_book_returned(loan)
	if not published:
		print("Warning: failed to publish book.returned event")
	return loan