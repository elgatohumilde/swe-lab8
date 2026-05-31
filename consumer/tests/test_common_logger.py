import logging

from app.common.logger import APP_LOGGER


class TestLogger:
    def test_app_logger_is_logger(self):
        assert isinstance(APP_LOGGER, logging.Logger)

    def test_app_logger_name(self):
        assert APP_LOGGER.name == "uvicorn"
