from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import get_db
from ..core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.models.sqlalchemy_models import Account  # adjust import path as needed
from sqlalchemy.future import select
from app.core.security import verify_password, hash_password
from sqlalchemy.orm import selectinload




router = APIRouter()

async def authenticate_user(db: AsyncSession, email: str, password: str):
    """Authenticate user by verifying email and password."""
    async with db.begin():
        result = await db.execute(select(Account).filter(Account.email == email))
        user = result.scalars().first()
        if user and verify_password(password, user.password):
            user_data = {
                'accountid': str(user.accountid),  # Ensure UUID is in a serializable format
                'email': user.email,
                'type': user.type,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'verified': user.verified
            }
            return user_data
    return None

@router.post("/api/auth/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Authenticate user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form containing 'username' and 'password'.
        db (AsyncSession): Database session dependency.

    Returns:
        dict: Token and token type if successful.

    Raises:
        HTTPException: If authentication fails.
    """
    # Replace `authenticate_user` with your actual user authentication logic against the database
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email'], "accountid": user['accountid']}, expires_delta=access_token_expires
    )
    return {"account_id": user['accountid'], "access_token": access_token, "token_type": "bearer"}

# DELETE ME
@router.get("/api/auth/tmp")
async def tmp():
    return {"this_is_a_hash": hash_password("securePassword123")}
