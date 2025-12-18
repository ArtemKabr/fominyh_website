# Makefile — команды для разработки и миграций

.PHONY: up down rebuild logs makemigrations migrate db-reset

up:
	docker compose up --build

down:
	docker compose down

rebuild:
	docker compose down -v
	docker compose up --build

logs:
	docker compose logs -f backend

makemigrations:
	docker compose run --rm backend alembic revision --autogenerate -m "$(m)"

migrate:
	docker compose run --rm backend alembic upgrade head

db-reset:
	docker compose down -v
	docker compose up --build


# Как этим пользоваться (запомни)

# Создать новую миграцию
# make makemigrations m="add booking status"
#

# Применить миграции
# make migrate
#

# Полный пересбор (БД + backend)
# make rebuild
#

# Обычный запуск
# make up
#

# Логи backend
# make logs
