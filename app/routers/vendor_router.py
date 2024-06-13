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
            password=hash_password(account_data.password),  # You should hash this password
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

# move this to account router
@router.delete("/api/vendor/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(account_data: AccountDelete, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    print('debug0')
    # Start a transaction
    async with db.begin():
        account_id = account_data.account_id
        print('debug1')
        # Check if the account exists
        account_stmt = select(Account).where(Account.accountid == account_id)
        print('debug2')
        account_result = await db.execute(account_stmt)
        print('debug3')
        retrieved_account = account_result.scalars().first()
        print('debug4')
        if not retrieved_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        if retrieved_account.email != current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and Username do not match")

        print('debug5')
        
        # Retrieve the vendor associated with this account
        vendor_stmt = select(Vendor).where(Vendor.accountid == account_id)
        vendor_result = await db.execute(vendor_stmt)
        vendor = vendor_result.scalars().first()

        # Delete all listings associated with this vendor
        if vendor:
            await db.execute(delete(Listing).where(Listing.vendorid == vendor.vendorid))
        
            # Delete the vendor
            await db.execute(delete(Vendor).where(Vendor.accountid == account_id))

        # Delete the account
        await db.execute(delete(Account).where(Account.accountid == account_id))

        # Commit the transaction
        await db.commit()

    return {"message": "Vendor Account and all related data deleted successfully"}

@router.post("/api/vendor/createListing")
async def create_listing(listing_data: ListingCreate, current_user: str = Depends(get_current_user)):
    title = listing_data.title
    # Your endpoint logic here
    return {"message": "Listing created", "user": current_user, "title" : title}
