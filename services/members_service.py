"""Member use cases."""
from database import db_session
from repositories import loans_repository, members_repository
from utils import checks, fines, validation


def list_members():
    with db_session() as conn:
        return members_repository.find_all(conn)


def get_member(member_id):
    with db_session() as conn:
        member = members_repository.find_by_id(conn, member_id)
    return checks.ensure_found(member, "member not found")


def create_member(data):
    name, email, member_type = validation.validate_member(data)
    with db_session() as conn:
        checks.ensure_email_unused(members_repository.find_by_email(conn, email))
        member_id = members_repository.insert(conn, name, email, member_type)
        return members_repository.find_by_id(conn, member_id)


def get_member_loans(member_id):
    with db_session() as conn:
        member = checks.ensure_found(members_repository.find_by_id(conn, member_id), "member not found")
        loans = loans_repository.find_by_member(conn, member_id)
    return {
        "loans": loans,
        "total_owed": fines.amount_owed(loans),
        "loans_remaining": checks.loans_remaining(member, loans),
    }
