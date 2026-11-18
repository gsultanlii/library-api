"""SQL for the members table."""
from database import row_to_dict


def find_all(conn):
    return [dict(r) for r in conn.execute("SELECT * FROM members").fetchall()]


def find_by_id(conn, member_id):
    return row_to_dict(conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone())


def find_by_email(conn, email):
    return row_to_dict(conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone())


def insert(conn, name, email, member_type):
    cur = conn.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
        (name, email, member_type),
    )
    return cur.lastrowid
