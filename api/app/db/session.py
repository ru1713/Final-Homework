from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://appuser:supersecret@localhost:5432/recruiting"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session