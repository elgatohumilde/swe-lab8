import os

from app.common.exceptions import MissingEnvVariableException


def load_env(var: str) -> str:
    env = os.getenv(var)

    if not env:
        raise MissingEnvVariableException(var)

    return env
