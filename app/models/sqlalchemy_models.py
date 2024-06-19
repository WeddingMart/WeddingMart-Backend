# app/models/sqlalchemy_models.py
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'
    
    accountid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Consider encrypting this in practice
    type = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    verificationid = Column(UUID(as_uuid=True), nullable=True)

    # Relationship to Vendor
    vendors = relationship("Vendors", back_populates="accounts", uselist=False)  # One-to-one relationship

class Vendors(Base):
    __tablename__ = 'vendors'
    
    vendorid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accountid = Column(UUID(as_uuid=True), ForeignKey('accounts.accountid'), nullable=False)
    vendorname = Column(String, nullable=False)
    
    # Relationship to Account
    accounts = relationship("Accounts", back_populates="vendors")

    # Relationship to Listing
    listings = relationship("Listings", back_populates="vendors")

class Listings(Base):
    __tablename__ = 'listings'
    
    listingid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String(2048))
    instagram = Column(String(2048))
    twitter = Column(String(2048))
    pinterest = Column(String(2048))
    spotify = Column(String(2048))
    soundcloud = Column(String(2048))
    facebook = Column(String(2048))
    listingcity = Column(String(50), nullable=False)
    listingstate = Column(String(2), nullable=False)
    listingcategory = Column(String(32), nullable=False)
    vendorid = Column(UUID(as_uuid=True), ForeignKey('vendors.vendorid'), nullable=False)

    # Relationship to Vendor
    vendors = relationship("Vendors", back_populates="listings")