import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# Позволяет запускать `alembic` из директории backend/ и находить internal.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from internal.core.config import settings  # noqa: E402
from internal.feature.db.models_registry import Base  # noqa: E402

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _sync_database_url() -> str:
    """
    Приложение использует асинхронный драйвер (postgresql+asyncpg) для
    рантайма, но Alembic по умолчанию работает синхронно — конвертируем
    URL на синхронный psycopg2 драйвер только для миграций. DATABASE_URL
    в .env остаётся один, ничего дополнительно настраивать не нужно.
    """
    url = settings.database_url
    if "+asyncpg" in url:
        return url.replace("+asyncpg", "+psycopg2")
    return url


config.set_main_option("sqlalchemy.url", _sync_database_url())


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
