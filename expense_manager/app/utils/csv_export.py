# app/utils/csv_export.py
"""Utility to generate CSV content from a list of Expense objects.
Returns a string that can be sent directly as a response body.
"""

import csv
import io
from typing import List
from ..models import Expense

def export_expenses_csv(expenses: List[Expense]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    # Header
    writer.writerow(["id", "amount", "description", "date", "category"])
    for e in expenses:
        writer.writerow([
            e.id,
            float(e.amount),
            e.description or "",
            e.date.isoformat(),
            e.category.name if e.category else "",
        ])
    return output.getvalue()