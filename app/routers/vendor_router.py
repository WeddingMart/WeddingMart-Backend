# app/routers/vendor_router.py

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
    AccountDelete, ListingEdit, AccountModel, VendorModel
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

# Vendor Routes
@router.post("/api/vendors", status_code=status.HTTP_201_CREATED)
async def create_account_and_vendor_endpoint(account_data: AccountCreate, vendor_data: VendorCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        new_account = await create_account(db, account_data)
        new_vendor = await create_vendor(db, new_account.accountid, vendor_data)
    return {"message": "Account and vendor created successfully"}

# get data about a specific vendor
@router.get("/api/vendors/{vendor_id}", status_code=status.HTTP_200_OK)
async def get_vendor_endpoint(vendor_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

# protected access vendor
@router.get("/api/accounts/{account_id}/vendors", response_model=VendorModel, status_code=status.HTTP_200_OK)
async def get_vendor_by_accountid_endpoint(account_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if account_id != current_user['accountid']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    async with db.begin():
        vendor = await get_vendor_by_accountid(db, account_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        
        return VendorModel(
            vendorid=vendor.vendorid,
            accountid=vendor.accountid,
            vendorname=vendor.vendorname
        )

@router.put("/api/vendors/{vendor_id}", status_code=status.HTTP_200_OK)
async def update_vendor_endpoint(vendor_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

@router.delete("/api/accounts/{account_id}/vendors", status_code=status.HTTP_200_OK)
async def delete_vendor_endpoint(account_id: UUID, account_data: AccountDelete, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if account_id != current_user['accountid']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    result = await delete_vendor_and_account(db, account_data.account_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or unauthorized")
    return {"message": "Vendor Account and all related data deleted successfully"}


