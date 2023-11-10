from rocketry import Rocketry
# from rocketry.args import Session
from rocketry.conds import daily, every, time_of_day
from app.core.configs import get_environment, get_logger
# from app.core.db import start_pool, PGConnection
# from app.core.db.redis_client import RedisClient
# from app.core.services import start_populate_neighborhood, start_populate_streets, CheckProperties
# from app.extractors import start_zap_imoveis_extractor, start_portal_imoveis_extractor
import requests
# import time


_env = get_environment()
_logger = get_logger(__name__)

app = Rocketry(config={"task_execution": "thread"})


@app.task(every("10 seconds"), based="finish")
async def health_check():
    _logger.info("I'm alive")


@app.task(daily & (time_of_day.at("04:00")), based="finish")
async def train_model():
    _logger.info(f"Checking if database needs to be populated")

    try:
        check_url = _env.GREY_WOLF_BASE_URL + "/models/train"
        response = requests.post(url=check_url)

        if response.status_code == 202:
            _logger.info(f"New model will be trained")
            return True

        else:
            _logger.info(f"Error on train new model")
            return True

    except Exception as error:
        _logger.error(f"Error on train_model: {str(error)}")
        return False
