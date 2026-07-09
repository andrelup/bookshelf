# BookShelf Backend — Hexagonal Architecture

API REST para tienda de libros. Este CLAUDE.md complementa el CLAUDE.md raíz del monorepo.

## Stack

- Python 3.12
- FastAPI (async)
- SQLAlchemy 2.0 (async, modelos declarativos)
- Alembic (migraciones autogeneradas)
- PostgreSQL 16 + pgvector (búsqueda semántica)
- pytest + pytest-asyncio + httpx (testing)
- structlog (logging estructurado)
- Ruff (linting + formatting)
- mypy strict (type checking)

## Arquitectura Hexagonal (Ports & Adapters)

```
backend/
├── src/
│   ├── domain/                    # NÚCLEO — lógica de negocio pura, sin dependencias externas
│   │   ├── models/                # Entidades de dominio (dataclasses o Pydantic BaseModel)
│   │   │   ├── user.py
│   │   │   ├── book.py
│   │   │   └── favourite.py
│   │   ├── ports/                 # Interfaces (Protocol classes) que el dominio expone
│   │   │   ├── repositories.py    # Ports de persistencia (UserRepository, BookRepository)
│   │   │   └── services.py        # Ports de servicios externos (EmbeddingService, LLMService)
│   │   ├── services/              # Casos de uso / lógica de negocio
│   │   │   ├── auth_service.py
│   │   │   ├── book_service.py
│   │   │   ├── search_service.py
│   │   │   └── recommendation_service.py
│   │   └── exceptions.py          # Excepciones de dominio (BookNotFoundError, UnauthorizedError, etc.)
│   │
│   ├── adapters/                  # ADAPTADORES — implementaciones concretas de los ports
│   │   ├── inbound/               # Adaptadores de entrada (cómo el mundo llama al dominio)
│   │   │   ├── api/               # FastAPI routes
│   │   │   │   ├── auth_router.py
│   │   │   │   ├── book_router.py
│   │   │   │   ├── search_router.py
│   │   │   │   ├── favourite_list_router.py
│   │   │   │   └── health_router.py
│   │   │   ├── schemas/           # Pydantic schemas (request/response de la API)
│   │   │   │   ├── auth_schemas.py
│   │   │   │   ├── book_schemas.py
│   │   │   │   └── common.py      # ApiResponse genérico
│   │   │   └── middleware/        # Auth middleware, logging middleware, CORS
│   │   │       ├── auth.py
│   │   │       ├── logging.py
│   │   │       └── error_handler.py
│   │   │
│   │   └── outbound/              # Adaptadores de salida (cómo el dominio accede al exterior)
│   │       ├── persistence/       # Implementaciones de repositorios
│   │       │   ├── sqlalchemy_models.py   # Modelos SQLAlchemy (ORM, separados del dominio)
│   │       │   ├── user_repository.py     # Implementa UserRepository port
│   │       │   ├── book_repository.py     # Implementa BookRepository port
│   │       │   └── database.py            # Engine, session factory, get_db dependency
│   │       ├── ai/                # Implementaciones de servicios de IA
│   │       │   ├── embedding_service.py   # Implementa EmbeddingService port
│   │       │   └── llm_service.py         # Implementa LLMService port
│   │       └── cache/
│   │           └── recommendation_cache.py
│   │
│   ├── config/                    # Configuración de la aplicación
│   │   ├── settings.py            # Pydantic Settings (env vars)
│   │   └── container.py           # Dependency injection (wiring ports → adapters)
│   │
│   └── main.py                    # Entrypoint FastAPI, registra routers y middleware
│
├── tests/
│   ├── conftest.py                # Fixtures globales: test DB, async client, usuarios
│   ├── unit/                      # Tests de domain/services (mocks de ports)
│   │   ├── test_auth_service.py
│   │   ├── test_book_service.py
│   │   └── test_search_service.py
│   ├── integration/               # Tests de adapters (con DB real de test)
│   │   ├── test_user_repository.py
│   │   └── test_book_repository.py
│   └── api/                       # Tests de endpoints (httpx.AsyncClient)
│       ├── test_auth_endpoints.py
│       ├── test_book_endpoints.py
│       └── test_search_endpoints.py
│
├── alembic/
│   ├── env.py
│   └── versions/
├── pyproject.toml
├── Dockerfile
└── seed.py
```

Nota: el `.pre-commit-config.yaml` vive en la **raíz del monorepo** (los git hooks son únicos por repositorio); los hooks del backend filtran con `files: ^backend/`.

## Reglas de Arquitectura Hexagonal

1. **El dominio NO importa de adapters.** Nunca. Los imports van siempre de fuera hacia dentro:
   - `adapters.inbound.api` → importa de `domain.services` y `domain.models`
   - `adapters.outbound.persistence` → importa de `domain.ports` e implementa sus interfaces
   - `domain.services` → importa de `domain.ports` y `domain.models`, NADA más

2. **Los ports son Protocol classes** (typing.Protocol), no clases abstractas:
   ```python
   from typing import Protocol

   class BookRepository(Protocol):
       async def find_by_id(self, book_id: int) -> Book | None: ...
       async def find_all(self, skip: int, limit: int) -> list[Book]: ...
       async def save(self, book: Book) -> Book: ...
       async def delete(self, book_id: int) -> None: ...
   ```

3. **Los modelos de dominio son independientes de SQLAlchemy.** Usa dataclasses o Pydantic BaseModel para el dominio. Los modelos SQLAlchemy viven en `adapters/outbound/persistence/sqlalchemy_models.py` y se mapean desde/hacia los modelos de dominio.

4. **Dependency injection en `config/container.py`.** Conecta los ports con sus implementaciones concretas. Los routers reciben los servicios de dominio ya inyectados via FastAPI Depends.

5. **Las excepciones de dominio se traducen en el error_handler middleware.** `BookNotFoundError` → HTTP 404, `UnauthorizedError` → HTTP 401, `ValidationError` → HTTP 422.

## Convenciones de código

- snake_case para todo (variables, funciones, archivos, módulos)
- PascalCase solo para clases (modelos, schemas, exceptions, protocols)
- Async/await en todos los endpoints, servicios y repositorios
- Type hints obligatorios en todas las funciones (mypy strict)
- Docstrings en servicios de dominio y funciones complejas
- Respuestas de la API siempre con formato:
  ```json
  {"success": true, "data": {...}, "error": null}
  {"success": false, "data": null, "error": "Book not found"}
  ```
- Schemas Pydantic separados por operación: `BookCreate`, `BookUpdate`, `BookResponse`, `BookListResponse`

## Testing

- Framework: pytest + pytest-asyncio + httpx.AsyncClient
- Patrón AAA: Arrange → Act → Assert (con comentarios)
- Fixtures centralizadas en `conftest.py`: test DB, async client, usuario autenticado (customer y seller)
- Tests unitarios: mockear los ports, testear servicios de dominio en aislamiento
- Tests de integración: usar DB real de test, verificar repositorios
- Tests de API: httpx.AsyncClient contra la app FastAPI
- Coverage mínimo: 80%
- Ejecutar: `pytest --cov=src --cov-report=term-missing`

## Migraciones

- Alembic con autogenerate desde modelos SQLAlchemy (no desde modelos de dominio)
- Crear migración: `alembic revision --autogenerate -m "descripción"`
- Aplicar: `alembic upgrade head`
- Rollback: `alembic downgrade -1`
- Siempre revisar el SQL generado antes de aplicar

## Logging

- structlog con JSON en producción, pretty-print en desarrollo
- Campos automáticos: timestamp, request_id, user_id, endpoint, method, status_code, duration_ms
- No usar `print()` nunca — siempre `logger.info()`, `logger.error()`, etc.

## Linting

- Ruff como linter y formatter único
- mypy en strict mode
- Pre-commit hooks: ruff check, ruff format, mypy

## Qué NO hacer

- No importar SQLAlchemy, FastAPI, httpx ni cualquier librería de infraestructura dentro de `domain/`
- No poner lógica de negocio en los routers — los routers solo validan input, llaman al servicio, y devuelven el response
- No usar `from sqlalchemy import ...` en `domain/services/`
- No crear endpoints sin su schema Pydantic correspondiente
- No hacer queries SQL directas — siempre a través del repositorio