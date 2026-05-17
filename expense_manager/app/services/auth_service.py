# app/services/auth_service.py
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

_revoked_tokens = set()

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def generate_tokens(user_id) -> dict:
    identity = str(user_id)
    access = create_access_token(identity=identity, expires_delta=timedelta(minutes=60))
    refresh = create_refresh_token(identity=identity, expires_delta=timedelta(days=7))
    return {"access_token": access, "refresh_token": refresh}

def revoke_token(jti: str):
    _revoked_tokens.add(jti)

def is_token_revoked(jti: str) -> bool:
    return jti in _revoked_tokens
