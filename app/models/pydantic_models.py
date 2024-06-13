# app/models/pydantic_models.py
from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from uuid import UUID

class AccountCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # Constrains the password to a minimum of 8 characters
    type: str
    firstname: str
    lastname: str

class VendorCreate(BaseModel):
    vendorname: str

class ListingCreate(BaseModel):
    title: constr(max_length=255)  # Assuming title can be optional and has a max length of 255
    description: Optional[constr(max_length=4098)] # length controlled by api
    instagram: Optional[constr(max_length=2048)]
    twitter: Optional[constr(max_length=2048)]
    pinterest: Optional[constr(max_length=2048)]
    spotify: Optional[constr(max_length=2048)]
    soundcloud: Optional[constr(max_length=2048)]
    facebook: Optional[constr(max_length=2048)]
    listingcity: constr(max_length=50)
    listingstate: constr(max_length=2)
    listingcategory: constr(max_length=32)

class AccountDelete(BaseModel):
    account_id: UUID