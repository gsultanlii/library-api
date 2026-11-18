"""Turn database dicts into the JSON shapes the API returns."""
from utils.fines import money


def book_json(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "available": bool(book["available"]),
    }


def member_json(member):
    return {
        "id": member["id"],
        "name": member["name"],
        "email": member["email"],
        "type": member["type"],
    }


def loan_json(loan):
    result = {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
        "renewals": loan["renewals"],
        "checked_out": loan["checked_out"],
    }
    if "current_fine" in loan:
        result["current_fine"] = money(loan["current_fine"])
    return result


def member_loan_json(loan):
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
    }
