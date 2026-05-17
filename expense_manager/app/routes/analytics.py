# app/routes/analytics.py
"""Blueprint exposing analytics endpoints for the dashboard.
Provides monthly spend summary and category breakdown for a given month.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.expense_service import monthly_summary, category_breakdown
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/monthly', methods=['GET'])
@jwt_required()
def get_monthly():
    user_id = get_jwt_identity()
    data = monthly_summary(user_id)
    return jsonify(data), 200

@analytics_bp.route('/category', methods=['GET'])
@jwt_required()
def get_category_breakdown():
    user_id = get_jwt_identity()
    month = request.args.get('month')
    year = request.args.get('year')
    if not month or not year:
        # default to current month
        now = datetime.utcnow()
        month = now.month
        year = now.year
    else:
        month = int(month)
        year = int(year)
    data = category_breakdown(user_id, month, year)
    return jsonify(data), 200