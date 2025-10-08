from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATA_BASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/nameless_chat"

engine = create_async_engine(DATA_BASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_async_session():
    async with async_session() as session:
        yield session