"""
Module to load all Environment variables
"""

from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # APPLICATION
    APPLICATION_HOST: str = "localhost"
    APPLICATION_PORT: int = 8000
    ADDRESS_BASE_URL: str = "localhost:8000"

    # DATABASE
    DATABASE_URL: str = "localhost:5432"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: str = "password"
    DATABASE_NAME: str = "test"
    ENVIRONMENT: str = "test"
    DATABASE_MIN_CONNECTIONS: int = 1
    DATABASE_MAX_CONNECTIONS: int = 1

    class Config:
        """Load config file"""

        env_file = ".env"
        extra='ignore'
