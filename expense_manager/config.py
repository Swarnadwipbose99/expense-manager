# config.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def _fix_db_url(url):
    """Render gives postgres:// but SQLAlchemy 1.4+ requires postgresql://"""
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = _fix_db_url(
        os.getenv("DATABASE_URL",
                  f"sqlite:///{os.path.abspath(os.path.join(basedir, 'instance', 'dev.db'))}")
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = _fix_db_url(os.getenv("DATABASE_URL"))
