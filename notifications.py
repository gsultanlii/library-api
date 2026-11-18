"""Notifications.

MockNotifier is a mock object (https://en.wikipedia.org/wiki/Mock_object): it stands in for a
real e-mail service. Instead of sending anything it appends a line to outbox.txt and remembers
every message in `sent`, so tests can check what would have been sent.
"""
import config


class MockNotifier:
    def __init__(self):
        self.sent = []

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        with open(config.OUTBOX_PATH, "a") as f:
            f.write(f"TO: {to} | SUBJECT: {subject} | BODY: {body}\n")

    def clear(self):
        self.sent.clear()


notifier = MockNotifier()


def notify_checkout(email, title):
    notifier.send(email, "Book checked out", "You checked out " + title)


def notify_renewal(email, title):
    notifier.send(email, "Loan renewed", "You renewed " + title)


def notify_return(email, title, fine):
    notifier.send(email, "Book returned", f"You returned {title}. Fine: ${fine}")


def notify_fine_paid(email, amount):
    notifier.send(email, "Fine paid", f"We received ${amount}")
