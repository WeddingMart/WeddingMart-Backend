# app/routers/vendor_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from sqlalchemy.sql import text
from sqlalchemy.future import select
from ..models.pydantic_models import AccountCreate, VendorCreate, ListingCreate, AccountDelete
from ..models.sqlalchemy_models import Account, Vendor, Listing  # Import your SQLAlchemy models
import uuid
from uuid import UUID
from app.core.auth import get_current_user
from app.core.security import hash_password
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete
from ..crud import create_account, create_vendor, delete_vendor_and_account, create_listing



router = APIRouter()

@router.get("/api/test")
async def read_items(db: AsyncSession = Depends(get_db)):
    return {"result" : "this is a test"}

@router.get("/api/vendor")
async def read_items(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(text("SELECT * FROM accounts"))
        items = result.scalars().all()
        return items

@router.post("/api/vendor/create", status_code=status.HTTP_201_CREATED)
async def create_account_and_vendor(account_data: AccountCreate, vendor_data: VendorCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        new_account = await create_account(db, account_data)
        new_vendor = await create_vendor(db, new_account.accountid, vendor_data)
    return {"message": "Account and vendor created successfully"}

@router.delete("/api/vendor/delete", status_code=status.HTTP_200_OK)
async def delete_vendor(account_data: AccountDelete, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    result = await delete_vendor_and_account(db, account_data.account_id, current_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or unauthorized")
    return {"message": "Vendor Account and all related data deleted successfully"}


@router.post("/api/vendor/createListing", status_code=status.HTTP_201_CREATED)
async def create_listing_endpoint(listing_data: ListingCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    async with db.begin():
        # Retrieve vendor ID based on current user
        vendor_stmt = select(Vendor).join(Account).where(Account.email == current_user)
        vendor_result = await db.execute(vendor_stmt)
        vendor = vendor_result.scalars().first()

        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

        # Create the listing using CRUD function
        listing = await create_listing(db, listing_data, vendor.vendorid)
        listingid = listing.listingid
    return {"message": "Listing created successfully", "listing_id": str(listingid)}
