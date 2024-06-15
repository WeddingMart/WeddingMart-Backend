# app/main.py
# Remember that all IO (SQL, S3, FastAPI) must be async

from fastapi import FastAPI
from .routers import tools_router, auth_router, account_router, vendor_router, listing_router

app = FastAPI()

app.include_router(tools_router.router)
app.include_router(auth_router.router)
app.include_router(account_router.router)
app.include_router(vendor_router.router)
app.include_router(listing_router.router)
