run:
	docker compose -f docker-compose.yaml up --force-recreate --remove-orphans

crun:
	docker compose -f docker-compose.yaml up --force-recreate --remove-orphans --build
