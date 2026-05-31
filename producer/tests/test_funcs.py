import pytest

from app.common.exceptions import MissingEnvVariableException
from app.common.funcs import load_env


class TestLoadEnv:
    def test_load_env_returns_value(self, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "test_value")
        assert load_env("TEST_VAR") == "test_value"

    def test_load_env_raises_when_missing(self):
        with pytest.raises(MissingEnvVariableException):
            load_env("NONEXISTENT_VAR_12345")
