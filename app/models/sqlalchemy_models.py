from sqlalchemy import Column, String, Boolean, ForeignKey
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
    vendors = relationship("Vendor", back_populates="account")

class Vendor(Base):
    __tablename__ = 'vendor'
    
    vendorid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accountid = Column(UUID(as_uuid=True), ForeignKey('account.accountid'), nullable=False)
    vendorname = Column(String, nullable=False)
    listingid = Column(UUID(as_uuid=True), nullable=True)

    # Relationship to Account
    account = relationship("Account", back_populates="vendors")
