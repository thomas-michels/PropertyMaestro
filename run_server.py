import logging
from asyncio import run
from app import start_application

if __name__ == "__main__":
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())
    run(start_application())
