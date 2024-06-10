# app/routers/item_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from sqlalchemy.sql import text


router = APIRouter()

@router.get("/items/")
async def read_items(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(text("SELECT * FROM accounts"))
        items = result.scalars().all()
        return items
