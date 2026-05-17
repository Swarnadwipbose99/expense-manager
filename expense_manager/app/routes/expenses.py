# app/routes/expenses.py
"""Blueprint exposing CRUD endpoints for expenses.
All routes require a valid JWT access token.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.expense_service import (
    create_expense,
    update_expense,
    delete_expense,
    list_expenses,
    monthly_summary,
    category_breakdown,
)
from ..utils.csv_export import export_expenses_csv
from datetime import datetime
from decimal import Decimal

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    category = request.args.get('category')
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    # Parse dates if provided
    start_date = datetime.strptime(start, "%Y-%m-%d").date() if start else None
    end_date = datetime.strptime(end, "%Y-%m-%d").date() if end else None
    expenses = list_expenses(user_id, category, start_date, end_date)
    result = [
        {
            "id": e.id,
            "amount": float(e.amount),
            "description": e.description,
            "date": e.date.isoformat(),
            "category": e.category.name,
        }
        for e in expenses
    ]
    return jsonify(result), 200

@expenses_bp.route('', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        amount = Decimal(str(data.get('amount')))
        description = data.get('description')
        expense_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
        category_name = data.get('category')
        expense = create_expense(user_id, amount, description, expense_date, category_name)
        return jsonify({"id": expense.id}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def edit_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        amount = Decimal(str(data['amount'])) if 'amount' in data else None
        description = data.get('description')
        expense_date = datetime.strptime(data['date'], "%Y-%m-%d").date() if 'date' in data else None
        category_name = data.get('category')
        expense = update_expense(
            expense_id,
            user_id,
            amount=amount,
            description=description,
            expense_date=expense_date,
            category_name=category_name,
        )
        return jsonify({"msg": "updated", "id": expense.id}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def remove_expense(expense_id):
    user_id = get_jwt_identity()
    try:
        delete_expense(expense_id, user_id)
        return jsonify({"msg": "deleted"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

@expenses_bp.route('/export', methods=['GET'])
@jwt_required()
def export_csv():
    user_id = get_jwt_identity()
    expenses = list_expenses(user_id)
    csv_content = export_expenses_csv(expenses)
    return (
        csv_content,
        200,
        {
            "Content-Type": "text/csv",
            "Content-Disposition": "attachment; filename=expenses.csv",
        },
    )
