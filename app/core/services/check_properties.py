from app.core.db import PGConnection
from app.core.configs import get_environment, get_logger
from app.core.db.redis_client import RedisClient
from app.producer.utils.event_schema import EventSchema
from app.producer import KombuProducer
from app.core.services.property_services import PropertyServices
from uuid import uuid4
from datetime import datetime

_env = get_environment()
_logger = get_logger(__name__)


class CheckProperties:

    def __init__(self, conn: PGConnection, redis_conn: RedisClient) -> None:
        self.conn = conn
        self.redis_conn = redis_conn

    def handle(self, message: EventSchema) -> bool:
        _logger.info("Checking properties")
        services = PropertyServices(conn=self.conn, redis_conn=self.redis_conn)
        if services.is_updating():
            _logger.info("Properties checked")
            return True

        services.set_updating(value=1)

        properties = services.search_all_actived_properties()
        _logger.info(f"Properties: {len(properties)}")

        if properties:
            for property in properties:
                if property["company"] == "portal_imoveis":
                    sent_to = _env.PORTAL_IMOVEIS_IN_CHANNEL

                else:
                    sent_to = _env.ZAP_IMOVEIS_IN_CHANNEL

                event = EventSchema(
                    id=str(uuid4()),
                    origin="MAESTRO",
                    sent_to=sent_to,
                    payload=property,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )

                KombuProducer.send_messages(conn=self.conn, message=event)

        _logger.info("Properties checked")
        return True
