import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Backend papkasini import yo'liga qo'shamiz (alembic/ ichida turganimiz uchun)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Barcha domain modellarni import qilamizki metadata to'liq bo'lsin
import db  # noqa: F401  (Base)
import users.models  # noqa: F401
import schools.models  # noqa: F401
import courses.models  # noqa: F401
import lessons.models  # noqa: F401
import enrollments.models  # noqa: F401
import homeworks.models  # noqa: F401
import quizzes.models  # noqa: F401
import notifications.models  # noqa: F401
import payments.models  # noqa: F401
import messages.models  # noqa: F401
import api_keys.models  # noqa: F401
import crm.models  # noqa: F401
import marketing.models  # noqa: F401
import bot.models  # noqa: F401
import videos.models  # noqa: F401

target_metadata = db.Base.metadata

# DATABASE_URL faqat muhit o'zgaruvchisidan olinadi (alembic.ini dagi sqlalchemy.url ishlatilmaydi)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
