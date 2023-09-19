from rocketry import Rocketry
from rocketry.args import Session
from rocketry.conds import daily, every
from app.core.configs import get_environment, get_logger
from app.core.db import start_pool, PGConnection
from app.core.db.redis_client import RedisClient
from app.core.services import start_populate_neighborhood, start_populate_streets, CheckProperties
from app.extractors import start_zap_imoveis_extractor, start_portal_imoveis_extractor
import requests


_env = get_environment()
_logger = get_logger(__name__)

app = Rocketry(config={"task_execution": "thread"})


@app.setup()
def starting_database(session=Session()):
    session.parameters.connection_pool=start_pool()

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

@app.task(daily.starting("01:00"), based="finish")
async def start_portal_imoveis(session=Session()):
    _logger.info("start_portal_imoveis")
    with session.parameters.connection_pool.connection() as conn:
        pg_connection = PGConnection(conn=conn)
        start_portal_imoveis_extractor(conn=pg_connection)

    _logger.info("Portal Imoveis task had ended")
    return True

@app.task(daily.starting("02:00"), based="finish")
async def start_zap_imoveis(session=Session()):
    _logger.info("start_zap_imoveis")
    with session.parameters.connection_pool.connection() as conn:
        pg_connection = PGConnection(conn=conn)
        start_zap_imoveis_extractor(conn=pg_connection)

    _logger.info("Zap Imoveis task had ended")
    return True

@app.task(daily.starting("00:15"), based="finish")
async def check_all_properties(session=Session()):
    _logger.info("check_all_properties")
    with session.parameters.connection_pool.connection() as conn:
        pg_connection = PGConnection(conn=conn)
        redis_conn = RedisClient()
        check = CheckProperties(conn=pg_connection, redis_conn=redis_conn)
        check.handle(None)

    _logger.info("All properties were checked")
    return True
