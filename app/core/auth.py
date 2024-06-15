# app/core/auth.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from uuid import UUID

# Configuration constants
SECRET_KEY = "your_secret_key_here"  # Secret key for encoding and decoding JWTs
ALGORITHM = "HS256"  # Algorithm used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Lifespan of the token

# Setting up OAuth2 with Password and Bearer (JWT) flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token that stores user information and has an expiry date.

    Args:
        data (dict): A dictionary with data to encode within the token.
        expires_delta (timedelta, optional): The amount of time until the token expires.

    Returns:
        str: A JWT token encoded as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Validate the JWT token and extract user identity.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): Exception to raise in case of failure.

    Returns:
        str: The user identity from the token payload.

    Raises:
        credentials_exception: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        accountid: int = payload.get("accountid")
        if username is None:
            raise credentials_exception
        return {"username": username, "accountid": UUID(accountid)}
    except jwt.PyJWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency that extracts and verifies the user from the token payload.

    Args:
        token (str): JWT token provided by the user.

    Returns:
        str: User identifier.

    Raises:
        HTTPException: With status 401 if token is invalid or if credentials are not valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
