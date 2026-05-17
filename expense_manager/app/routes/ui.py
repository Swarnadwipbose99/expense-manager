# app/routes/ui.py
"""Blueprint that serves the HTML pages of the Expense Manager UI."""

from flask import Blueprint, render_template

ui_bp = Blueprint('ui', __name__)


@ui_bp.route('/')
def home():
    return render_template('login.html')


@ui_bp.route('/login')
def login_page():
    return render_template('login.html')


@ui_bp.route('/signup')
def signup_page():
    return render_template('signup.html')


@ui_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@ui_bp.route('/expenses/new')
def new_expense():
    return render_template('expense_form.html')


@ui_bp.route('/expenses/<int:expense_id>/edit')
def edit_expense(expense_id):
    return render_template('expense_form.html', expense_id=expense_id)
