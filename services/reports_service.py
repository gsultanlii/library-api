"""Report use cases."""
from database import db_session
from repositories import books_repository, loans_repository
from utils import fines


def overdue_report():
    with db_session() as conn:
        rows = loans_repository.find_open_with_details(conn)
    items = []
    total = 0
    for r in rows:
        late = fines.days_late(r["due_date"])
        if late > 0:
            fine = fines.fine_for_days(late)
            total += fine
            items.append(
                {
                    "loan_id": r["loan_id"],
                    "title": r["title"],
                    "member": r["member"],
                    "days_late": late,
                    "fine": fines.money(fine),
                }
            )
    return {"items": items, "total_fines": fines.money(total)}


def summary_report():
    with db_session() as conn:
        total_books = books_repository.count(conn)
        loans = loans_repository.find_all(conn)
    return {
        "total_books": total_books,
        "on_loan": sum(1 for loan in loans if not loan["returned"]),
        "fines_outstanding": fines.money(fines.amount_owed(loans)),
    }
