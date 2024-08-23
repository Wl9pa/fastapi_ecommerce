from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import *
from sqlalchemy import insert, select, update
from app.schemas import CreateReview

router = APIRouter(prefix='/review', tags=['review'])


@router.get('/all_reviews')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    ratings = await db.scalars(select(Rating).where(Rating.is_active == True))
    return {
        'reviews': reviews.all(),
        'ratings': ratings.all()
    }


@router.get('/products_reviews/{product_id}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id,
                                                    Review.is_active == True))
    ratings = await db.scalars(select(Rating).where(Rating.product_id == product_id,
                                                    Rating.is_active == True))
