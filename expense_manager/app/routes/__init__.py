# app/routes/__init__.py
"""Package for route blueprints.
Each module defines a Flask Blueprint that is imported in the app factory.
"""

# The individual route modules (auth, expenses, analytics) expose
# variables `auth_bp`, `expenses_bp`, `analytics_bp` respectively.
