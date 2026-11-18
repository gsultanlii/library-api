"""Unit tests that need no HTTP and no database."""
import os
import tempfile
import unittest
from datetime import date

import config
import notifications
from utils import fines


class FineTests(unittest.TestCase):
    def test_fine_is_half_a_dollar_per_late_day(self):
        self.assertEqual(fines.fine_for_days(5), 2.5)

    def test_no_fine_when_not_late(self):
        self.assertEqual(fines.fine_for_days(-3), 0)

    def test_amount_owed(self):
        loans = [
            {"returned": 0, "due_date": "2026-11-13", "fine": 0, "fine_paid": 0},
            {"returned": 1, "due_date": "2026-01-01", "fine": 1.0, "fine_paid": 0},
            {"returned": 1, "due_date": "2026-01-01", "fine": 9.0, "fine_paid": 1},
        ]
        self.assertEqual(fines.amount_owed(loans, today=date(2026, 11, 18)), 3.5)


class MockNotifierTests(unittest.TestCase):
    def test_records_message_and_writes_outbox(self):
        old = config.OUTBOX_PATH
        with tempfile.TemporaryDirectory() as d:
            config.OUTBOX_PATH = os.path.join(d, "outbox.txt")
            try:
                notifications.notifier.clear()
                notifications.notify_checkout("a@b.edu", "Clean Code")
                self.assertEqual(notifications.notifier.sent[0]["subject"], "Book checked out")
                with open(config.OUTBOX_PATH) as f:
                    self.assertIn("TO: a@b.edu", f.read())
            finally:
                config.OUTBOX_PATH = old


if __name__ == "__main__":
    unittest.main()
