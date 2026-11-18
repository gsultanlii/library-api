"""All business constants live here so each rule is defined in exactly one place."""

DB_PATH = "library.db"          # relative path: created in the folder the API runs from
OUTBOX_PATH = "outbox.txt"      # stands in for a real mail server

LOAN_DAYS = 14
RENEWAL_DAYS = 14
MAX_RENEWALS = 1
FINE_PER_DAY = 0.50

LOAN_LIMITS = {"student": 3, "staff": 5}
DEFAULT_LOAN_LIMIT = 3
MEMBER_TYPES = ("student", "staff")
