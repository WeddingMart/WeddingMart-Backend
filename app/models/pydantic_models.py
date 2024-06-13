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
    title: str

class AccountDelete(BaseModel):
    account_id: UUID