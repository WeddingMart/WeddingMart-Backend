# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.sqlalchemy_models import Account, Vendor, Listing
from app.core.security import hash_password

async def create_account(db: AsyncSession, account_data):
    new_account = Account(
        email=account_data.email,
        password=hash_password(account_data.password),
        type=account_data.type,
        firstname=account_data.firstname,
        lastname=account_data.lastname
    )
    db.add(new_account)
    await db.flush()  # Flushing to get the generated accountid
    return new_account

async def create_vendor(db: AsyncSession, account_id, vendor_data):
    new_vendor = Vendor(
        accountid=account_id,
        vendorname=vendor_data.vendorname
    )
    db.add(new_vendor)
    await db.flush()
    return new_vendor

async def delete_vendor_and_account(db: AsyncSession, account_id, current_user):
    account_stmt = select(Account).where(Account.accountid == account_id)
    account_result = await db.execute(account_stmt)
    retrieved_account = account_result.scalars().first()
    if not retrieved_account or retrieved_account.email != current_user:
        return None

    # Retrieve the vendor associated with the account_id
    vendor_stmt = select(Vendor).where(Vendor.accountid == account_id)
    vendor_result = await db.execute(vendor_stmt)
    vendor = vendor_result.scalars().first()

    if not vendor:
        return None

    await db.execute(delete(Listing).where(Listing.vendorid == vendor.vendorid))
    await db.execute(delete(Vendor).where(Vendor.accountid == account_id))
    await db.execute(delete(Account).where(Account.accountid == account_id))
    await db.commit()
    return "Deleted"

async def create_listing(db: AsyncSession, listing_data, vendor_id):
    new_listing = Listing(
        title=listing_data.title,
        description=listing_data.description,
        instagram=listing_data.instagram,
        twitter=listing_data.twitter,
        pinterest=listing_data.pinterest,
        spotify=listing_data.spotify,
        soundcloud=listing_data.soundcloud,
        facebook=listing_data.facebook,
        listingcity=listing_data.listingcity,
        listingstate=listing_data.listingstate,
        listingcategory=listing_data.listingcategory,
        vendorid=vendor_id
    )
    db.add(new_listing)
    await db.flush()
    return new_listing