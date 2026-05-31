from sqlalchemy import Engine

from app.config.db_engine import ENGINE, create_db_and_tables


class TestDbEngine:
    def test_engine_is_engine(self):
        assert isinstance(ENGINE, Engine)

    def test_create_db_and_tables(self):
        create_db_and_tables()
