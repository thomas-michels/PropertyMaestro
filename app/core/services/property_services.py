from typing import List
from app.core.db import PGConnection
from app.core.db.redis_client import RedisClient


class PropertyServices:

    def __init__(self, conn: PGConnection, redis_conn: RedisClient) -> None:
        self.__conn = conn
        self.__redis_conn = redis_conn

    def set_updating(self, value: int) -> bool:
        self.__redis_conn.conn.setex(name="is_updating", value=value, time=3000)

    def is_updating(self) -> bool:
        return bool(self.__redis_conn.conn.get("is_updating"))

    def search_all_actived_properties(self) -> List[str]:
        query = """
        SELECT
            DISTINCT property_url,
            c."name" AS company
        FROM
            public.properties p
        INNER JOIN public.companies c ON
            p.company_id = c.id
        WHERE
            is_active IS TRUE;
        """

        results = self.__conn.execute(sql_statement=query, all=True)

        properties = []

        if results:
            for result in results:
                cached_on_redis = self.__redis_conn.conn.get(result["property_url"])

                if not cached_on_redis:
                    properties.append({
                        "property_url": result["property_url"],
                        "company": result["company"],
                    })

        return properties
