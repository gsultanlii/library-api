from flask import Blueprint, jsonify, request

from services import members_service
from utils.fines import money
from utils.serializers import member_json, member_loan_json

bp = Blueprint("members", __name__)


@bp.route("/members", methods=["GET"])
def list_members():
    return jsonify([member_json(m) for m in members_service.list_members()])


@bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    return jsonify(member_json(members_service.get_member(member_id)))


@bp.route("/members", methods=["POST"])
def create_member():
    data = request.get_json(silent=True) or {}
    return jsonify(member_json(members_service.create_member(data))), 201


@bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    result = members_service.get_member_loans(member_id)
    return jsonify(
        {
            "loans": [member_loan_json(loan) for loan in result["loans"]],
            "total_owed": money(result["total_owed"]),
            "loans_remaining": result["loans_remaining"],
        }
    )
