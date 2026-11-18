"""SQL for the loans table."""
from database import row_to_dict


def find_all(conn):
    return [dict(r) for r in conn.execute("SELECT * FROM loans").fetchall()]


def find_by_id(conn, loan_id):
    return row_to_dict(conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone())


def find_by_member(conn, member_id):
    rows = conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()
    return [dict(r) for r in rows]


def find_open_with_details(conn):
    rows = conn.execute(
        """
        SELECT loans.id AS loan_id, books.title AS title, members.name AS member,
               loans.due_date AS due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()
    return [dict(r) for r in rows]


def insert(conn, book_id, member_id, due_date, checked_out):
    cur = conn.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
        (book_id, member_id, due_date, checked_out),
    )
    return cur.lastrowid


def mark_returned(conn, loan_id, fine):
    conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))


def renew(conn, loan_id, new_due_date):
    conn.execute(
        "UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?",
        (new_due_date, loan_id),
    )


def mark_fine_paid(conn, loan_id):
    conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
