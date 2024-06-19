# app/routers/client_router.py

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