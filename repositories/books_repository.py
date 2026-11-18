"""SQL for the books table. Nothing else in the project writes book SQL."""
from database import row_to_dict


def find_all(conn, only_available=False):
    if only_available:
        rows = conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
    else:
        rows = conn.execute("SELECT * FROM books").fetchall()
    return [dict(r) for r in rows]


def find_by_id(conn, book_id):
    return row_to_dict(conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone())


def insert(conn, title, author, isbn):
    cur = conn.execute(
        "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
        (title, author, isbn),
    )
    return cur.lastrowid


def delete(conn, book_id):
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))


def set_available(conn, book_id, available):
    conn.execute("UPDATE books SET available = ? WHERE id = ?", (1 if available else 0, book_id))


def count(conn):
    return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
