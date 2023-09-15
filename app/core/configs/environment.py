"""
Module to load all Environment variables
"""

from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # APPLICATION
    ADDRESS_BASE_URL: str = "localhost:8000"

    # RABBIT
    RBMQ_HOST: str
    RBMQ_USER: str
    RBMQ_PASS: str
    RBMQ_PORT: int
    RBMQ_EXCHANGE: str
    RBMQ_VHOST: str
    PREFETCH_VALUE: int

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

    # PORTAIS
    PORTAL_IMOVEIS_URL: str
    ZAP_IMOVEIS_URL: str
    ZAP_IMOVEIS_BASE_URL: str

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: str
    TIMED_CACHE: int

    # Queues
    ZAP_IMOVEIS_IN_CHANNEL: str
    PORTAL_IMOVEIS_IN_CHANNEL: str

    class Config:
        """Load config file"""

        env_file = ".env"
        extra='ignore'
