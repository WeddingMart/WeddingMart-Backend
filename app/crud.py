# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.sqlalchemy_models import Accounts, Vendors, Listings
from app.core.security import hash_password
# from uuid import UUID

async def create_account(db: AsyncSession, account_data):
    new_account = Accounts(
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
    new_vendor = Vendors(
        accountid=account_id,
        vendorname=vendor_data.vendorname
    )
    db.add(new_vendor)
    await db.flush()
    return new_vendor

async def delete_vendor_and_account(db: AsyncSession, account_id):
    account_stmt = select(Accounts).where(Accounts.accountid == account_id)
    account_result = await db.execute(account_stmt)
    retrieved_account = account_result.scalars().first()
    if not retrieved_account:
        return None

    # Retrieve the vendor associated with the account_id
    vendor_stmt = select(Vendors).where(Vendors.accountid == account_id)
    vendor_result = await db.execute(vendor_stmt)
    vendor = vendor_result.scalars().first()

    if not vendor:
        return None

    await db.execute(delete(Listings).where(Listings.vendorid == vendor.vendorid))
    await db.execute(delete(Vendors).where(Vendors.accountid == account_id))
    await db.execute(delete(Accounts).where(Accounts.accountid == account_id))
    await db.commit()
    return "Deleted"

async def create_listing(db: AsyncSession, listing_data, vendor_id):
    new_listing = Listings(
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

async def edit_listing(db: AsyncSession, listing_data, vendor_id, listing_id):
    query = select(Listings).where(Listings.listingid == listing_id)
    result = await db.execute(query)
    listing = result.scalars().one_or_none()

    if not listing:
        return None
    if listing.vendorid != vendor_id:
        return None

    for field, value in listing_data.dict(exclude_unset=True).items():
        setattr(listing, field, value)
    
    await db.flush()
    await db.refresh(listing)
    return listing

async def get_account_by_accountid(db: AsyncSession, account_id):
    query = select(Accounts).where(Accounts.accountid == account_id)
    result = await db.execute(query)
    account = result.scalars().first()
    if not account:
        return None
    return account

async def get_vendor_by_vendorid(db: AsyncSession, vendor_id): # unused
    query = select(Vendors).where(Vendors.vendorid == vendor_id)
    result = await db.execute(query)
    vendor = result.scalars().first()
    if not vendor:
        return None
    return vendor

async def get_vendor_by_accountid(db: AsyncSession, account_id):
    query = select(Vendors).where(Vendors.accountid == account_id)
    result = await db.execute(query)
    vendor = result.scalars().first()
    return vendor

# async def get_listings_by_vendor(db: AsyncSession, vendor_id):
#     query = select(Listings).where(Listings.vendorid == vendor_id)
#     result = await db.execute(query)
#     listings = result.scalars().all()
#     return listings