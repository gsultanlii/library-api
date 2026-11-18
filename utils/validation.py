"""Input validation: is the data well formed? (Business rules live in checks.py.)"""
import re
from datetime import date

import config
from errors import AppError


def is_valid_email(value):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(value)) is not None


def is_valid_isbn(value):
    digits = str(value).replace("-", "")
    return digits.isdigit() and len(digits) in (10, 13)


def is_valid_date(value):
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def is_valid_member_type(value):
    return value in config.MEMBER_TYPES


def validate_book(data):
    if not data.get("title") or not data.get("author"):
        raise AppError("title and author are required", 400)
    if not is_valid_isbn(data.get("isbn")):
        raise AppError("invalid isbn", 400)
    return data["title"], data["author"], data["isbn"]


def validate_member(data):
    if not data.get("name"):
        raise AppError("name is required", 400)
    if not is_valid_email(data.get("email")):
        raise AppError("invalid email", 400)
    member_type = data.get("type", "student")
    if not is_valid_member_type(member_type):
        raise AppError("type must be student or staff", 400)
    return data["name"], data["email"], member_type


def validate_loan(data):
    if not data.get("book_id") or not data.get("member_id"):
        raise AppError("book_id and member_id are required", 400)
    if data.get("due_date") and not is_valid_date(data["due_date"]):
        raise AppError("invalid due_date", 400)
    return data["book_id"], data["member_id"], data.get("due_date") or None
