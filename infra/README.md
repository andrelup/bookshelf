# Infraestructura BookShelf

Servicios de infraestructura del proyecto vía Docker Compose. De momento: PostgreSQL 16 con la extensión pgvector.

## Requisitos

- Docker Desktop en marcha.
- `backend/.env` creado (copia `backend/.env.example` y rellena los valores). Las credenciales de la BD **nunca** se versionan ni se hardcodean en el compose.

## Uso

Desde este directorio (`infra/`):

```bash
# Levantar la BD (lee credenciales de backend/.env)
docker compose --env-file ../backend/.env up -d

# Estado y salud del contenedor
docker compose --env-file ../backend/.env ps

# Parar (los datos persisten en el volumen postgres_data)
docker compose --env-file ../backend/.env down

# Parar Y BORRAR los datos
docker compose --env-file ../backend/.env down -v
```

## Verificar

```bash
# Salud del contenedor
docker inspect --format '{{.State.Health.Status}}' bookshelf-postgres   # → healthy

# Conexión desde el backend (desde backend/, con el venv activado)
alembic upgrade head
```

La extensión pgvector se habilita automáticamente en el primer arranque mediante `postgres/init/01-pgvector.sql`.
