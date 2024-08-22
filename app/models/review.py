from app.backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    comment = Column(String)
    comment_date = Column(DateTime, default=func.now)
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')
    ratings = relationship('Rating', back_populates='reviews')
