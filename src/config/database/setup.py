
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings import dev_settings, prod_settings, base_setting

async def create_engine():
    if base_setting.DEBUG == True:
        engine = await create_async_engine(url=dev_settings.DATABASE_URL, echo=False)
    else:
        engine = await create_async_engine(url=prod_settings.DATABASE_URL, echo=False)
    return engine

async def make_session():
    session = await async_sessionmaker(
        bind=create_engine(), 
        expire_on_commit=False, 
        auto_flush=False)
    return session

async def get_db():
    db = await make_session()
    try:
        yield db
    finally:
        db.close()



