# app/main.py
# Remember that all IO (SQL, S3, FastAPI) must be async

from fastapi import FastAPI
from .routers import item_router, vendor_router, auth_router

app = FastAPI()

app.include_router(item_router.router)
app.include_router(vendor_router.router)
app.include_router(auth_router.router)
