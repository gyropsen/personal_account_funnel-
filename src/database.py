from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import load_config

config = load_config()

# Движок
async_engine = create_async_engine(
    url=config.data_base.database_url_asyncpg,
)
# Сессия
async_session_factory = async_sessionmaker(async_engine)
