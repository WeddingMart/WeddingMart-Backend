# app/models/sqlalchemy_models.py
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    
    accountid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Consider encrypting this in practice
    type = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    verificationid = Column(UUID(as_uuid=True), nullable=True)

    # Relationship to Vendor
    vendors = relationship("Vendor", back_populates="account", uselist=False)  # One-to-one relationship

class Vendor(Base):
    __tablename__ = 'vendor'
    
    vendorid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accountid = Column(UUID(as_uuid=True), ForeignKey('account.accountid'), nullable=False)
    vendorname = Column(String, nullable=False)
    
    # Relationship to Account
    account = relationship("Account", back_populates="vendors")

    # Relationship to Listing
    listings = relationship("Listing", back_populates="vendor")

class Listing(Base):
    __tablename__ = 'listing'
    
    listingid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instagram = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    pinterest = Column(String, nullable=True)
    spotify = Column(String, nullable=True)
    soundcloud = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    listingcity = Column(String, nullable=False)
    listingstate = Column(String, nullable=False)
    listingcategory = Column(String, nullable=False)

    # Foreign key to Vendor
    vendorid = Column(UUID(as_uuid=True), ForeignKey('vendor.vendorid'), nullable=False)

    # Relationship to Vendor
    vendor = relationship("Vendor", back_populates="listings")