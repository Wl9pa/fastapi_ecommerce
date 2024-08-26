from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import *
from sqlalchemy import insert, select, update, func
from app.schemas import CreateReview
from datetime import datetime

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
    product = await db.scalar(select(Product.id).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id,
                                                    Review.is_active == True))
    ratings = await db.scalars(select(Rating).where(Rating.product_id == product_id,
                                                    Rating.is_active == True))
    return {
        'reviews': reviews.all(),
        'ratings': ratings.all()
    }


@router.post('/add_review', status_code=status.HTTP_201_CREATED)
async def add_reviews(db: Annotated[AsyncSession, Depends(get_db)], review_data: CreateReview,
                      get_user: Annotated[dict, Depends(get_current_user)], product_id: int, ):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    if get_user.get('is_customer'):
        new_review = Review(user_id=get_user.get('id'), product_id=product_id, comment=review_data.comment,
                            comment_date=datetime.now(), is_active=True)
        new_rating = Rating(user_id=get_user.get('id'), product_id=product_id, grade=review_data.grade, is_active=True)
        db.add_all([new_review, new_rating])
        await db.commit()

        all_ratings = await db.scalars(select(Rating.grade).where(Rating.product_id == product_id,
                                                                  Rating.is_active == True))
        all_ratings_list = all_ratings.all()
        if len(all_ratings_list) > 0:
            average_rating = sum(all_ratings_list) / len(all_ratings_list)
            await db.execute(update(Product).where(Product.id == product_id).values(rating=average_rating))
            await db.commit()
        return {
            'message': 'Review and rating added successfully'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only customers can add reviews'
        )


@router.delete('/delete_review/{review_id}', status_code=status.HTTP_200_OK)
async def delete_reviews(review_id: int, db: Annotated[AsyncSession, Depends(get_db)],
                         get_user: Annotated[dict, Depends(get_current_user)]):
    review = await db.scalar(select(Review).where(Review.id == review_id))
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found'
        )
    product_id = review.product_id
    user_id = review.user_id
    if get_user.get('is_admin'):
        await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
        await db.execute(update(Rating).where(Rating.product_id == product_id,
                                          Rating.user_id == user_id).values(is_active=False))
        grades = await db.scalars(select(Rating.grade).where(Rating.product_id == review.product_id,
                                                             Rating.is_active == True))
        grade_list = grades.all()
        updated_rating = sum(grade_list) / len(grade_list) if grade_list else 0
        await db.execute(update(Product).where(Product.id == review.product_id).values(rating=updated_rating))
        await db.commit()
        return {
            'message': 'Review and rating deactivated'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )
