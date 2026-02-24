from typing import List, Optional
from datetime import datetime

from . import models

_loans: List[models.Loan] = []
_next_id = 1


def create_loan(loan_create: models.LoanCreate) -> models.Loan:
	global _next_id
	loan = models.Loan(
		id=_next_id,
		book_id=loan_create.book_id,
		borrower=loan_create.borrower,
		active=True,
		started_at=datetime.utcnow(),
		returned_at=None,
	)
	_loans.append(loan)
	_next_id += 1
	return loan


def list_loans() -> List[models.Loan]:
	return _loans.copy()


def close_loan(loan_id: int) -> Optional[models.Loan]:
	"""Mark the loan as closed: set active False and returned_at timestamp."""
	for i, l in enumerate(_loans):
		if l.id == loan_id and l.active:
			updated = models.Loan(
				id=l.id,
				book_id=l.book_id,
				borrower=l.borrower,
				active=False,
				started_at=l.started_at,
				returned_at=datetime.utcnow(),
			)
			_loans[i] = updated
			return updated
	return None
