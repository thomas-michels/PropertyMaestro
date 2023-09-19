from datetime import datetime
import requests
from app.core.configs import get_logger, get_environment

_logger = get_logger(__name__)
_env = get_environment()


def start_populate_neighborhood():
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    with open("data/neighbors.csv", "r", encoding="UTF-8") as neighbor_file:
        neighbors = []

        for row in neighbor_file.readlines():
            row = row.strip().split(";")
            neighbors.append(
                {"name": row[0], "population": row[1], "houses": row[2], "area": row[3]}
            )

    start = datetime.now()
    count = 0
    for data in neighbors:
        try:
            requests.post(
                url=f"{_env.ADDRESS_BASE_URL}/neighborhoods", json=data, headers=headers
            )
            _logger.info(data["name"])
            count += 1

        except Exception as error:
            _logger.info(str(error))

    _logger.info(count)
    _logger.info(datetime.now() - start)


if __name__ == "__main__":
    start_populate_neighborhood()
