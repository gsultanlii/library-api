"""Error handling: one place that turns problems into JSON error responses."""
from flask import jsonify


class AppError(Exception):
    """Raised anywhere in the code; converted to a JSON response by the handler below."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def error_response(message, status_code):
    """Build a JSON error response from a custom message and an HTTP status code."""
    return jsonify({"error": message}), status_code


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err):
        return error_response(err.message, err.status_code)
