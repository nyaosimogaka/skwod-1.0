from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.settings import settings

# Create async engine
engine = create_async_engine(
    settings.DB_PATH,
    echo=True,             # Turn off in production
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
