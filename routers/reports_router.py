from flask import Blueprint, jsonify

from services import reports_service

bp = Blueprint("reports", __name__)


@bp.route("/reports/overdue", methods=["GET"])
def report_overdue():
    return jsonify(reports_service.overdue_report())


@bp.route("/reports/summary", methods=["GET"])
def report_summary():
    return jsonify(reports_service.summary_report())
