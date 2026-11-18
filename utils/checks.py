"""Business-rule checks. Each one raises AppError when a library rule is broken."""
from datetime import date

import config
from errors import AppError
from utils import fines


def ensure_found(entity, message):
    if entity is None:
        raise AppError(message, 404)
    return entity


def ensure_book_available(book):
    if book["available"] == 0:
        raise AppError("book is not available", 409)


def ensure_book_not_on_loan(book):
    if book["available"] == 0:
        raise AppError("book is on loan", 409)


def ensure_email_unused(existing_member):
    if existing_member is not None:
        raise AppError("email already registered", 409)


def loan_limit_for(member_type):
    return config.LOAN_LIMITS.get(member_type, config.DEFAULT_LOAN_LIMIT)


def open_loan_count(loans):
    return sum(1 for loan in loans if not loan["returned"])


def loans_remaining(member, loans):
    return loan_limit_for(member["type"]) - open_loan_count(loans)


def ensure_no_unpaid_fines(loans):
    if fines.amount_owed(loans) > 0:
        raise AppError("member has unpaid fines", 409)


def ensure_under_loan_limit(member, loans):
    if open_loan_count(loans) >= loan_limit_for(member["type"]):
        raise AppError("loan limit reached", 409)


def ensure_loan_open(loan):
    if loan["returned"] == 1:
        raise AppError("loan already returned", 409)


def ensure_renewable(loan, today=None):
    today = today or date.today()
    ensure_loan_open(loan)
    if date.fromisoformat(loan["due_date"]) < today:
        raise AppError("overdue loans cannot be renewed", 409)
    if loan["renewals"] >= config.MAX_RENEWALS:
        raise AppError("loan was already renewed", 409)


def ensure_fine_payable(loan):
    if loan["returned"] == 0:
        raise AppError("return the book before paying", 409)
    if loan["fine"] <= 0 or loan["fine_paid"] == 1:
        raise AppError("no fine to pay", 409)
