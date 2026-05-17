# app/services/expense_service.py
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import List, Optional, Dict
from ..models import db, Expense, Category
from sqlalchemy import func


def get_or_create_category(user_id, name: str) -> Category:
    user_id = int(user_id)
    cat = Category.query.filter_by(user_id=user_id, name=name).first()
    if not cat:
        cat = Category(name=name, user_id=user_id)
        db.session.add(cat)
        db.session.commit()
    return cat


def create_expense(user_id, amount, description, expense_date, category_name):
    user_id = int(user_id)
    cat = get_or_create_category(user_id, category_name)
    exp = Expense(amount=amount, description=description, date=expense_date,
                  category_id=cat.id, user_id=user_id)
    db.session.add(exp)
    db.session.commit()
    return exp


def update_expense(expense_id, user_id, amount=None, description=None,
                   expense_date=None, category_name=None):
    user_id = int(user_id)
    exp = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if not exp:
        raise ValueError("Expense not found")
    if amount is not None:
        exp.amount = amount
    if description is not None:
        exp.description = description
    if expense_date is not None:
        exp.date = expense_date
    if category_name is not None:
        cat = get_or_create_category(user_id, category_name)
        exp.category_id = cat.id
    db.session.commit()
    return exp


def delete_expense(expense_id, user_id):
    user_id = int(user_id)
    exp = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if not exp:
        raise ValueError("Expense not found")
    db.session.delete(exp)
    db.session.commit()


def list_expenses(user_id, category=None, start_date=None, end_date=None):
    user_id = int(user_id)
    q = Expense.query.filter_by(user_id=user_id)
    if category:
        q = q.join(Category).filter(Category.name == category)
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    return q.order_by(Expense.date.desc()).all()


def monthly_summary(user_id):
    """Return total spend per month for last 12 months.
    Works on both SQLite (dev) and PostgreSQL (production).
    """
    user_id = int(user_id)
    one_year_ago = (datetime.utcnow() - timedelta(days=365)).date()

    dialect = db.engine.dialect.name
    if dialect == 'sqlite':
        year_col  = func.strftime('%Y', Expense.date).label('year')
        month_col = func.strftime('%m', Expense.date).label('month')
    else:  # postgresql
        year_col  = func.extract('year',  Expense.date).cast(db.Integer).label('year')
        month_col = func.extract('month', Expense.date).cast(db.Integer).label('month')

    rows = (
        db.session.query(
            year_col, month_col,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count'),
        )
        .filter(Expense.user_id == user_id, Expense.date >= one_year_ago)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    return [{"year": int(r.year), "month": int(r.month),
             "total": float(r.total), "count": int(r.count)} for r in rows]


def category_breakdown(user_id, month, year):
    user_id = int(user_id)
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    rows = (
        db.session.query(Category.name, func.sum(Expense.amount).label('total'))
        .join(Expense)
        .filter(Expense.user_id == user_id,
                Expense.date >= start, Expense.date < end)
        .group_by(Category.name)
        .all()
    )
    return [{"category": r[0], "total": float(r[1])} for r in rows]
