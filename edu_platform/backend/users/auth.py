import os

from pwdlib import PasswordHash

from pwdlib.hashers.bcrypt import BcryptHasher

from jose import jwt

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

pwd_context = PasswordHash((BcryptHasher(),))

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:

    raise RuntimeError("SECRET_KEY environment variable is required")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 7))

def hash_password(password: str) -> str:

    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:

    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str, role: str, **kwargs) -> str:

    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    payload = {"sub": str(user_id), "role": role, "exp": expire}

    payload.update(kwargs)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

