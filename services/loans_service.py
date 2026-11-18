"""Loan use cases: checkout, return, renew, pay a fine."""
from datetime import date, timedelta

import config
import notifications
from database import db_session
from repositories import books_repository, loans_repository, members_repository
from utils import checks, fines, validation


def _with_current_fine(loan):
    return {**loan, "current_fine": fines.current_fine(loan)}


def list_loans(overdue_only=False):
    with db_session() as conn:
        loans = loans_repository.find_all(conn)
    result = []
    for loan in loans:
        if overdue_only and (loan["returned"] == 1 or fines.days_late(loan["due_date"]) <= 0):
            continue
        result.append(_with_current_fine(loan))
    return result


def get_loan(loan_id):
    with db_session() as conn:
        loan = loans_repository.find_by_id(conn, loan_id)
    return _with_current_fine(checks.ensure_found(loan, "loan not found"))


def create_loan(data):
    book_id, member_id, due_date = validation.validate_loan(data)
    with db_session() as conn:
        book = checks.ensure_found(books_repository.find_by_id(conn, book_id), "book not found")
        member = checks.ensure_found(members_repository.find_by_id(conn, member_id), "member not found")
        checks.ensure_book_available(book)

        member_loans = loans_repository.find_by_member(conn, member_id)
        checks.ensure_no_unpaid_fines(member_loans)
        checks.ensure_under_loan_limit(member, member_loans)

        today = date.today()
        due_date = due_date or (today + timedelta(days=config.LOAN_DAYS)).isoformat()
        loan_id = loans_repository.insert(conn, book_id, member_id, due_date, today.isoformat())
        books_repository.set_available(conn, book_id, False)
        loan = loans_repository.find_by_id(conn, loan_id)

    notifications.notify_checkout(member["email"], book["title"])
    return loan


def return_book(loan_id):
    with db_session() as conn:
        loan = checks.ensure_found(loans_repository.find_by_id(conn, loan_id), "loan not found")
        checks.ensure_loan_open(loan)

        fine = fines.fine_for_due_date(loan["due_date"])
        loans_repository.mark_returned(conn, loan_id, fine)
        books_repository.set_available(conn, loan["book_id"], True)
        member = members_repository.find_by_id(conn, loan["member_id"])
        book = books_repository.find_by_id(conn, loan["book_id"])
        updated = loans_repository.find_by_id(conn, loan_id)

    notifications.notify_return(member["email"], book["title"], fines.money(fine))
    return updated


def renew_loan(loan_id):
    with db_session() as conn:
        loan = checks.ensure_found(loans_repository.find_by_id(conn, loan_id), "loan not found")
        checks.ensure_renewable(loan)

        new_due = (date.fromisoformat(loan["due_date"]) + timedelta(days=config.RENEWAL_DAYS)).isoformat()
        loans_repository.renew(conn, loan_id, new_due)
        member = members_repository.find_by_id(conn, loan["member_id"])
        book = books_repository.find_by_id(conn, loan["book_id"])
        updated = loans_repository.find_by_id(conn, loan_id)

    notifications.notify_renewal(member["email"], book["title"])
    return updated


def pay_fine(loan_id):
    with db_session() as conn:
        loan = checks.ensure_found(loans_repository.find_by_id(conn, loan_id), "loan not found")
        checks.ensure_fine_payable(loan)

        loans_repository.mark_fine_paid(conn, loan_id)
        member = members_repository.find_by_id(conn, loan["member_id"])
        updated = loans_repository.find_by_id(conn, loan_id)

    notifications.notify_fine_paid(member["email"], fines.money(loan["fine"]))
    return updated
