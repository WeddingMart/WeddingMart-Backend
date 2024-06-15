# app/models/pydantic_models.py
from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from uuid import UUID

class AccountModel(BaseModel):
    accountid: UUID
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    type: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    verified: Optional[bool] = None
    verificationid: Optional[UUID] = None

class VendorModel(BaseModel):
    vendorid: UUID
    accountid: UUID
    vendorname: Optional[str] = None


class AccountCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # Constrains the password to a minimum of 8 characters
    type: str
    firstname: str
    lastname: str

class VendorCreate(BaseModel):
    vendorname: str

class ListingCreate(BaseModel):
    title: Optional[constr(max_length=255)] = None  # Assuming title can be optional and has a max length of 255
    description: Optional[constr(max_length=4098)] = None  # Length controlled by API
    instagram: Optional[constr(max_length=2048)] = None
    twitter: Optional[constr(max_length=2048)] = None
    pinterest: Optional[constr(max_length=2048)] = None
    spotify: Optional[constr(max_length=2048)] = None
    soundcloud: Optional[constr(max_length=2048)] = None
    facebook: Optional[constr(max_length=2048)] = None
    listingcity: Optional[constr(max_length=50)] = None
    listingstate: Optional[constr(max_length=2)] = None
    listingcategory: Optional[constr(max_length=32)] = None

class AccountDelete(BaseModel):
    account_id: UUID

class ListingEdit(BaseModel):
    listingid: UUID
    title: Optional[constr(max_length=255)] = None
    description: Optional[constr(max_length=4098)] = None
    instagram: Optional[constr(max_length=255)] = None
    twitter: Optional[constr(max_length=255)] = None
    pinterest: Optional[constr(max_length=255)] = None
    spotify: Optional[constr(max_length=255)] = None
    soundcloud: Optional[constr(max_length=255)] = None
    facebook: Optional[constr(max_length=255)] = None
    listingcity: Optional[constr(max_length=255)] = None
    listingstate: Optional[constr(max_length=255)] = None
    listingcategory: Optional[constr(max_length=255)] = None