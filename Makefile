setup:
	cp .env.template .env
	make build

build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

restart-server:
	docker compose restart server

restart-worker:
	docker compose restart worker

stop:
	docker compose stop

migrate:
	docker compose run --rm server alembic upgrade head

migrations:
	docker compose run --rm server alembic revision --autogenerate
