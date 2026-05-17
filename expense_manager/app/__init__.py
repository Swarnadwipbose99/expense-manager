# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_wtf import CSRFProtect
import logging

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
csrf = CSRFProtect()

def create_app(config_object="expense_manager.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    csrf.init_app(app)

    from .routes import auth, expenses, analytics
    csrf.exempt(auth.auth_bp)
    csrf.exempt(expenses.expenses_bp)
    csrf.exempt(analytics.analytics_bp)

    app.register_blueprint(auth.auth_bp,         url_prefix="/api/v1/auth")
    app.register_blueprint(expenses.expenses_bp,  url_prefix="/api/v1/expenses")
    app.register_blueprint(analytics.analytics_bp, url_prefix="/api/v1/analytics")

    from .routes import ui
    app.register_blueprint(ui.ui_bp)

    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    return app
