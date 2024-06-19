# app/routers/listing_router.py

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

# Listing Routes
@router.post("/api/accounts/{account_id}/vendors/listings", status_code=status.HTTP_201_CREATED)
async def create_listing_endpoint(account_id: UUID, listing_data: ListingCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if account_id != current_user['accountid']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    async with db.begin():
        # Retrieve vendor ID based on current user
        vendor_stmt = select(Vendors).join(Accounts).where(Accounts.accountid == account_id)
        vendor_result = await db.execute(vendor_stmt)
        vendor = vendor_result.scalars().first()

        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

        # Create the listing using CRUD function
        listing = await create_listing(db, listing_data, vendor.vendorid)
        listingid = listing.listingid
    return {"message": "Listing created successfully", "listing_id": str(listingid)}

@router.get("/api/listings", status_code=status.HTTP_200_OK)
async def get_listings_endpoint(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

@router.get("/api/listings/{listing_id}", status_code=status.HTTP_200_OK)
async def get_listing_endpoint(listing_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

@router.put("/api/accounts/{account_id}/vendors/listings/{listing_id}", status_code=status.HTTP_200_OK)
async def update_listing_endpoint(account_id: UUID, listing_id: UUID, listing_data: ListingEdit, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if account_id != current_user['accountid']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    async with db.begin():
        # Retrieve vendor ID based on current user
        vendor_stmt = select(Vendors).join(Accounts).where(Accounts.accountid == account_id)
        vendor_result = await db.execute(vendor_stmt)
        vendor = vendor_result.scalars().first()

        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        
        updated_listing = await edit_listing(db, listing_data, vendor.vendorid, listing_id)

        if not updated_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found or Vendor does not have access to listing")
    return {"message": "Listing updated successfully"}

@router.delete("/api/listing/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing_endpoint(listing_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return {}

# @router.get("/api/vendor/{vendor_id}/listings", response_model=List[ListingEdit], status_code=status.HTTP_200_OK) # BROKEN
# async def get_vendor_listings_endpoint(vendor_id: UUID, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
#     listings = await get_listings_by_vendor(db, vendor_id)
#     return listings