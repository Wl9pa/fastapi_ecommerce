Проект интернет магазина на FastAPI
Запуск:
  1. docker compose -f docker-compose.prod.yml up -d --build - сборка образа и поднятие контейнеров
  2. docker compose -f docker-compose.prod.yml exec web alembic upgrade head - миграция для создания структуры бд
Остановка:
  docker stop <ID_or_NAME>
Остановка и удаление:
  docker compose -f docker-compose.prod.yml down -v
