# app/routers/account_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID, uuid4

from ..database import get_db
from ..models.pydantic_models import (
    AccountCreate, VendorCreate, ListingCreate,
    AccountDelete, ListingEdit, AccountModel, VendorModel,
    AccountUpdate
)
from ..models.sqlalchemy_models import Accounts, Vendors, Listings
from ..crud import (
    create_account, create_vendor, delete_vendor_and_account,
    create_listing, edit_listing, get_account_by_accountid,
    get_vendor_by_vendorid, get_vendor_by_accountid
)
from app.core.auth import get_current_user
from app.core.security import hash_password

router = APIRouter()

# Account Routes
@router.post("/api/accounts", status_code=status.HTTP_201_CREATED)
async def create_account_endpoint(account: AccountCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

@router.get("/api/accounts/{account_id}", status_code=status.HTTP_200_OK)
async def get_account_endpoint(account_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if account_id != current_user['accountid']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    async with db.begin():
        account = await get_account_by_accountid(db, account_id)
        if not account: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        
        return AccountModel(
            accountid=account.accountid,
            email=account.email,
            password=None,
            type=account.type,
            firstname=account.firstname,
            lastname=account.lastname,
            verified=account.verified,
            verificationid=account.verificationid
        )

@router.put("/api/accounts/{account_id}", status_code=status.HTTP_200_OK)
async def update_account_endpoint(account_id: UUID, updated_account: AccountUpdate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

@router.delete("/api/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account_endpoint(account_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}
