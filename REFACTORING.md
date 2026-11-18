# Refactoring notes

## Structure
```
app.py            creates the app, registers routers, keeps `app` and `init_db`
config.py         all constants (fine rate, loan days, limits, file paths)
database.py       connection, db_session(), init_db()
errors.py         AppError + error_response(message, status_code)
notifications.py  MockNotifier (writes outbox.txt, records messages in memory)
routers/          books, members, loans, reports   (HTTP only)
services/         books, members, loans, reports   (use cases / business logic)
repositories/     books, members, loans            (SQL only)
utils/            validation.py, checks.py, fines.py, serializers.py
```

## Problems found in the old app.py
1. All layers mixed in every handler (HTTP + SQL + rules): low cohesion.
2. SQL inside every route handler: routes depend on the DB schema.
3. The fine rate 0.50 appeared in several places: one change needed many edits.
4. The owed-amount loop was copied 3 times (member loans, checkout, summary).
5. Global `CURRENT_MEMBER` used by `notify()`: hidden coupling between handlers.
6. Notifications written in two different ways (helper vs direct file writes).
7. Row access by index (`loan[4]`, `loan[6]`): unreadable and fragile.
8. The same JSON dict was built by hand 8+ times.

## Answers
- Most cohesive module: `utils/fines.py`. Its one job is to calculate fines.
- Removed dependency: handlers no longer depend on SQL or on a global; the fine rule
  and the notification channel can change independently.
- Remaining coupling: services call the repositories and the notification module
  directly. Accepted to keep the project simple.
