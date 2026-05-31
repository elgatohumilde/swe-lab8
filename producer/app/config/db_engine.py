from typing import Final

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from app.common.funcs import load_env

ENGINE: Final[Engine] = create_engine(
    load_env("PRODUCER_DB_URL"),
    connect_args={
        "check_same_thread": False,
    },
)


def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)
