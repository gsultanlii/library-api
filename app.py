import os

from flask import Flask

import config
from database import init_db  # noqa: F401  (re-exported: tests import init_db from app)
from errors import register_error_handlers
from routers import books_router, loans_router, members_router, reports_router

app = Flask(__name__)

for router in (books_router, members_router, loans_router, reports_router):
    app.register_blueprint(router.bp)

register_error_handlers(app)

if not os.path.exists(config.DB_PATH):
    init_db()
