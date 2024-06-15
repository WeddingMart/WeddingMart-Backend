# app/routers/vendor_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from sqlalchemy.sql import text
from sqlalchemy.future import select
from ..models.pydantic_models import AccountCreate, VendorCreate, ListingCreate, AccountDelete, ListingEdit, AccountModel, VendorModel
from ..models.sqlalchemy_models import Account, Vendor, Listing  # Import your SQLAlchemy models
import uuid
from uuid import UUID
from app.core.auth import get_current_user
from app.core.security import hash_password
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete
from ..crud import create_account, create_vendor, delete_vendor_and_account, create_listing, edit_listing, get_account_by_accountid, get_vendor_by_vendorid, get_vendor_by_accountid
from typing import List



router = APIRouter()

@router.get("/api/test")
async def test_endpoint(db: AsyncSession = Depends(get_db)):
    return {"result" : "this is a test"}

@router.get("/api/vendor")
async def read_items_endpoint(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(text("SELECT * FROM account"))
        items = result.scalars().all()
        return items

@router.post("/api/vendor/create", status_code=status.HTTP_201_CREATED)
async def create_account_and_vendor_endpoint(account_data: AccountCreate, vendor_data: VendorCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        new_account = await create_account(db, account_data)
        new_vendor = await create_vendor(db, new_account.accountid, vendor_data)
    return {"message": "Account and vendor created successfully"}

@router.delete("/api/vendor/delete", status_code=status.HTTP_200_OK)
async def delete_vendor_endpoint(account_data: AccountDelete, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
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

@router.get("/api/account/{account_id}/", status_code=status.HTTP_200_OK)
async def get_account_endpoint(account_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
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

# @router.get("/api/vendor/{vendor_id}/", response_model=VendorModel, status_code=status.HTTP_200_OK)
# async def get_vendor_endpoint(vendor_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
#     async with db.begin():
#         vendor = await get_vendor_by_vendorid(db, vendor_id)
#         if not vendor: 
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        
#         return VendorModel(
#             vendorid=vendor.vendorid,
#             accountid=vendor.accountid,
#             vendorname=vendor.vendorname
#         )

@router.get("/api/account/{account_id}/vendor", response_model=VendorModel, status_code=status.HTTP_200_OK)
async def get_vendor_by_accountid_endpoint(account_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    async with db.begin():
        vendor = await get_vendor_by_accountid(db, account_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        
        return VendorModel(
            vendorid=vendor.vendorid,
            accountid=vendor.accountid,
            vendorname=vendor.vendorname
        )

# @router.get("/api/vendor/{vendor_id}/listings", response_model=List[ListingEdit], status_code=status.HTTP_200_OK) # BROKEN
# async def get_vendor_listings_endpoint(vendor_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
#     listings = await get_listings_by_vendor(db, vendor_id)
#     return listings

@router.put("/api/listing/edit", status_code=status.HTTP_200_OK)
async def edit_listing_endpoint(listing_data: ListingEdit, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    async with db.begin():
        # Retrieve vendor ID based on current user
        vendor_stmt = select(Vendor).join(Account).where(Account.email == current_user)
        vendor_result = await db.execute(vendor_stmt)
        vendor = vendor_result.scalars().first()

        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        
        updated_listing = await edit_listing(db, listing_data, vendor.vendorid)

        if not updated_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found or Vendor does not have access to listing")
    return {"message": "Listing updated successfully"}

