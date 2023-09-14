from rocketry import Rocketry
from rocketry.conds import daily, every
from app.core.configs import get_environment, get_logger
from app.core.services import start_populate_neighborhood, start_populate_streets
import requests


_env = get_environment()
_logger = get_logger(__name__)

app = Rocketry(config={"task_execution": "thread"})

@app.task(every("10 seconds"), based="finish")
async def health_check():
    _logger.info("I'm alive")

@app.task(daily.starting("00:00"), based="finish")
async def populate_database():
    _logger.info(f"Checking if database needs to be populated")

    try:
        check_url = _env.ADDRESS_BASE_URL + "/address/zip-code/89066-040"
        response = requests.get(url=check_url)

        if response.status_code == 200:
            _logger.info(f"Database already populated")
            return True

        else:
            _logger.info(f"Starting to populate neighborhoods")
            start_populate_neighborhood()

            _logger.info(f"Starting to populate streets")
            start_populate_streets()
            return True

    except Exception as error:
        _logger.error(f"Error on populate_database: {str(error)}")
        return False
