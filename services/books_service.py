"""Book use cases."""
from database import db_session
from repositories import books_repository
from utils import checks, validation


def list_books(available_only=False):
    with db_session() as conn:
        return books_repository.find_all(conn, available_only)


def get_book(book_id):
    with db_session() as conn:
        book = books_repository.find_by_id(conn, book_id)
    return checks.ensure_found(book, "book not found")


def create_book(data):
    title, author, isbn = validation.validate_book(data)
    with db_session() as conn:
        book_id = books_repository.insert(conn, title, author, isbn)
        return books_repository.find_by_id(conn, book_id)


def delete_book(book_id):
    with db_session() as conn:
        book = checks.ensure_found(books_repository.find_by_id(conn, book_id), "book not found")
        checks.ensure_book_not_on_loan(book)
        books_repository.delete(conn, book_id)
