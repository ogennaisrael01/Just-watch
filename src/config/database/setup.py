
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession
)
from src.config.settings import dev_settings, prod_settings, base_setting

DATABASE_URL = (
    dev_settings.DATABASE_URL
    if base_setting.DEBUG
    else prod_settings.DATABASE_URL
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
    
    



