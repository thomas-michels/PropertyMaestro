include ./.env

build:
	docker build -t property_maestro --no-cache .

run:
	docker run --env-file .env --network ${DEV_CONTAINER_NETWORK} --name property_maestro -d property_maestro
