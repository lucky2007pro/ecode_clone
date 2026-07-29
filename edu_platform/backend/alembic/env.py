import asyncio

import os

import sys

from logging.config import fileConfig

from pathlib import Path

from sqlalchemy import pool

from sqlalchemy.engine import Connection

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

config = context.config

if config.config_file_name is not None:

    fileConfig(config.config_file_name)

import db

import users.models

import schools.models

import courses.models

import lessons.models

import enrollments.models

import homeworks.models

import quizzes.models

import notifications.models

import payments.models

import messages.models

import api_keys.models

import crm.models

import marketing.models

import bot.models

import videos.models

target_metadata = db.Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:

    raise RuntimeError("DATABASE_URL environment variable is required")

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

