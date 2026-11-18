"""Fine calculation. Pure functions: no HTTP, no database."""
from datetime import date

import config


def money(x):
    return round(float(x), 2)


def days_late(due_date, today=None):
    today = today or date.today()
    return (today - date.fromisoformat(due_date)).days


def fine_for_days(days):
    return max(0, days) * config.FINE_PER_DAY


def fine_for_due_date(due_date, today=None):
    return fine_for_days(days_late(due_date, today))


def current_fine(loan, today=None):
    """Open loans accrue a fine every day; returned loans keep the fine saved at return."""
    if not loan["returned"]:
        return fine_for_due_date(loan["due_date"], today)
    return loan["fine"]


def amount_owed(loans, today=None):
    """Accruing fines on open loans plus unpaid fines on returned loans."""
    owed = 0
    for loan in loans:
        if not loan["returned"]:
            owed += fine_for_due_date(loan["due_date"], today)
        elif not loan["fine_paid"]:
            owed += loan["fine"]
    return owed
