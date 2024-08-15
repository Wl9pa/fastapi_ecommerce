from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


# engine = create_engine('sqlite:///ecommerce.db', echo=True)
# SessionLocal = sessionmaker(bind=engine)
engine = create_async_engine('postgresql+asyncpg://ecommerce:ecommercep@localhost:5432/ecommerce', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
