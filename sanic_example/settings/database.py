from os import environ
import asyncpg
from sqlalchemy import create_engine, databases, inspect
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DB_USER = environ.get('DB_USER', 'postgres')
DB_PASSWORD = environ.get('DB_PASS', 'postgres')
DB_HOST = environ.get('DB_HOST', 'localhost')

TESTING = environ.get("TESTING", True)

if TESTING:
    # Use separate DB for tests
    DB_NAME = "postgres"
    TEST_SQLALCHEMY_DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    database = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL)
else:
    DB_NAME = "postgres"
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    database = create_async_engine(SQLALCHEMY_DATABASE_URL)