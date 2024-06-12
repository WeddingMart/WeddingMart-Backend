# app/routers/vendor_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from sqlalchemy.sql import text
from sqlalchemy.future import select
from ..models.pydantic_models import AccountCreate, VendorCreate, ListingCreate
from ..models.sqlalchemy_models import Account, Vendor  # Import your SQLAlchemy models
import uuid
from app.core.auth import get_current_user


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
        # Create new account
        new_account = Account(
            email=account_data.email,
            password=account_data.password,  # You should hash this password
            type=account_data.type,
            firstname=account_data.firstname,
            lastname=account_data.lastname
        )
        db.add(new_account)
        await db.flush()  # Flushing to get the generated accountid

        # Create new vendor associated with the account
        new_vendor = Vendor(
            accountid=new_account.accountid,
            vendorname=vendor_data.vendorname
        )
        db.add(new_vendor)
        await db.flush()

    return {"message": "Account and vendor created successfully"}

# Assuming /api/vendor/createListing is defined in your vendor_router.py

@router.post("/api/vendor/createListing")
async def create_listing(listing_data: ListingCreate, current_user: str = Depends(get_current_user)):
    title = listing_data.title
    # Your endpoint logic here
    return {"message": "Listing created", "user": current_user, "title" : title}
