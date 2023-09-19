from datetime import datetime
import requests
from app.core.configs import get_logger, get_environment

_logger = get_logger(__name__)
_env = get_environment()


def start_populate_streets():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    with open("data/flood_quota.csv", "r") as flood_file:
        flood_data = {}

        for row in flood_file:
            row = row.strip().split(";")
            zip_code = row[0]
            flood_data[zip_code] = {
                "zip_code": zip_code,
                "neighborhood": row[1],
                "street": row[2],
                "latitude": row[3],
                "longitude": row[4],
                "flood_quota": float(row[5])
            }

    with open("data/zip_codes_coordinates.csv", "r") as coordinates_file:
        for row in coordinates_file:
            row = row.strip().split(";")
            zip_code = row[0]

            if not flood_data.get(zip_code):
                flood_data[zip_code] = {
                "zip_code": zip_code,
                "neighborhood": row[1],
                "street": row[2],
                "latitude": row[3],
                "longitude": row[4],
                "flood_quota": None
            }
    
    start = datetime.now()
    count = 0
    for data in flood_data.values():
        try:
            requests.post(url=f"{_env.ADDRESS_BASE_URL}/address", json=data, headers=headers)
            _logger.info(data["street"])
            count += 1

        except Exception as error:
            _logger.info(str(error))

    _logger.info(count)
    _logger.info(datetime.now() - start)

if __name__ == "__main__":
    start_populate_streets()
