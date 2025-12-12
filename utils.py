import bcrypt
import jwt
import datetime
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
from .config import settings

# Token extraction for protected routes
security = HTTPBearer()

# ---------------------------------------
# PASSWORD FUNCTIONS
# ---------------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------------------------------
# JWT TOKEN CREATE & VERIFY
# ---------------------------------------
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    # sometimes token gives bytes - convert to str
    if isinstance(token, bytes):
        token = token.decode()

    return token


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------------------------------
# ONLY LOGGED-IN ADMIN CAN ACCESS SOME APIs
# ---------------------------------------
async def get_current_admin(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = decode_token(token)

    if "admin_id" not in payload or "organization" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token details")

    return payload
