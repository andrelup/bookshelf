# BookShelf — Tienda de libros con IA

Monorepo con backend Python y frontend React. Proyecto de formación en Claude Code y desarrollo agéntico.

## Estructura del repositorio

```
bookshelf/
├── backend/          # API REST — Python 3.12, FastAPI, Hexagonal Architecture
├── frontend/         # SPA — React 18, TypeScript, Bulletproof React Architecture
├── infra/            # Docker Compose, Prometheus, Grafana, SonarQube
├── .claude/          # Subagentes y slash commands
├── .github/          # GitHub Actions workflows
└── Makefile          # Comandos unificados del proyecto
```

Cada subdirectorio (`backend/`, `frontend/`) tiene su propio CLAUDE.md con convenciones específicas de su stack. Este archivo solo contiene reglas globales compartidas.

## Convenciones globales

- Idioma del código: inglés (variables, funciones, clases, comentarios)
- Idioma de documentación: español
- Type hints / tipos estrictos obligatorios en ambos stacks
- Todo el código debe tener tests. Coverage mínimo: 80%

## Git

- Conventional commits obligatorios: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `ci:`
- Scope del commit indica el módulo: `feat(backend): add book search endpoint`, `fix(frontend): fix login redirect`
- Una rama por feature: `feature/nombre-corto`
- PRs contra `main`, siempre con tests pasando

## Docker

- `docker-compose.yml` en `infra/` levanta todo el entorno
- Servicios: PostgreSQL 16, backend FastAPI, frontend React (dev), Prometheus, Grafana
- Dockerfiles multi-stage en cada subdirectorio (`backend/Dockerfile`, `frontend/Dockerfile`)
- Hot reload habilitado en desarrollo vía volúmenes

## Makefile (raíz)

Todos los comandos se ejecutan desde la raíz del monorepo:

```
make dev          → docker compose up (todo el entorno)
make test         → tests backend + frontend
make test-back    → solo tests backend
make test-front   → solo tests frontend
make test-e2e     → playwright tests
make lint         → linters backend + frontend
make migrate      → alembic upgrade head
make seed         → script de seed de datos
make build        → docker build de ambas imágenes
```

## Secretos y configuración

- Variables de entorno en `.env` (no versionado)
- `.env.example` versionado con todas las variables necesarias y valores de ejemplo
- Nunca hardcodear secrets, URLs de base de datos, API keys ni tokens en el código

## CI/CD

- GitHub Actions en `.github/workflows/`
- Pipeline: lint → test-backend → test-frontend → test-e2e → build → security-scan
- SonarQube como quality gate en PRs

## Qué NO hacer

- No importar código directamente entre `backend/` y `frontend/` — son proyectos independientes conectados por API REST
- No instalar dependencias globales — cada subdirectorio gestiona las suyas
- No hacer commits sin que los pre-commit hooks pasen
- No usar `print()` para debugging — usar el sistema de logging configurado (structlog en backend)