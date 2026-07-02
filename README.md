# BookShelf — Tienda de libros online

BookShelf es una tienda online de libros. Ofrece las mismas funcionalidades principales que esperarías de cualquier tienda de comercio electrónico moderna: registro e inicio de sesión de usuarios, navegación y búsqueda en el catálogo, compra de libros, consulta del histórico de compras, guardado de favoritos y más.

Es un **monorepo** con el backend y el frontend juntos, pensado como proyecto de formación en Claude Code y desarrollo agéntico. Aunque ambos conviven en el mismo repositorio, se **despliegan por separado**.

## Funcionalidades

- **Registro e inicio de sesión** — creación de cuenta e inicio de sesión seguro con JWT.
- **Catálogo y búsqueda** — navegación por el catálogo y búsqueda por título, autor o categoría, con búsqueda semántica mediante `pgvector`.
- **Compra** — añadir libros al carrito y completar la compra.
- **Histórico de compras** — consulta de pedidos anteriores.
- **Favoritos (wishlist)** — guardado de libros en una lista personal.
- **Recomendaciones** — sugerencias basadas en IA.
- **Rol de vendedor (seller)** — panel para gestionar el catálogo de libros propios.

## Estructura del repositorio

```
bookshelf/
├── backend/          # API REST — Python 3.12, FastAPI, Arquitectura Hexagonal
├── frontend/         # SPA — React 18, TypeScript, Bulletproof React Architecture
├── infra/            # Docker Compose, Prometheus, Grafana, SonarQube
├── .claude/          # Subagentes y slash commands
├── .github/          # GitHub Actions workflows
└── Makefile          # Comandos unificados del proyecto
```

Cada subdirectorio (`backend/`, `frontend/`) tiene su propio `README.md` y `CLAUDE.md` con las convenciones específicas de su stack. Este documento recoge únicamente la información global compartida.

## Stack tecnológico

| Capa        | Tecnologías                                                              |
| ----------- | ------------------------------------------------------------------------ |
| Frontend    | React 18, TypeScript, Vite, TailwindCSS, React Router v6                 |
| Backend     | Python 3.12, FastAPI (async), SQLAlchemy 2.0, Alembic                    |
| Base de datos | PostgreSQL 16 + pgvector                                               |
| Testing     | pytest / Vitest / Playwright (E2E)                                       |
| Infra       | Docker Compose, Prometheus, Grafana, SonarQube                           |
| CI/CD       | GitHub Actions                                                           |

Los dos proyectos son **independientes** y se comunican exclusivamente a través de la **API REST**; nunca comparten código directamente.

## Puesta en marcha

Requisitos: Docker y Docker Compose.

```bash
# 1. Copiar la plantilla de variables de entorno
cp .env.example .env

# 2. Levantar todo el entorno (PostgreSQL, backend, frontend, Prometheus, Grafana)
make dev

# 3. Aplicar migraciones y datos de ejemplo
make migrate
make seed
```

Con hot reload habilitado en desarrollo mediante volúmenes, los cambios en `backend/` y `frontend/` se recargan automáticamente.

## Comandos (Makefile)

Todos los comandos se ejecutan desde la raíz del monorepo:

| Comando           | Descripción                                     |
| ----------------- | ----------------------------------------------- |
| `make dev`        | `docker compose up` — levanta todo el entorno   |
| `make test`       | Tests de backend + frontend                     |
| `make test-back`  | Solo tests del backend                          |
| `make test-front` | Solo tests del frontend                         |
| `make test-e2e`   | Tests E2E con Playwright                         |
| `make lint`       | Linters de backend + frontend                   |
| `make migrate`    | `alembic upgrade head`                          |
| `make seed`       | Script de seed de datos                          |
| `make build`      | Build de las imágenes Docker de ambos proyectos |

## Convenciones globales

- **Idioma del código:** inglés (variables, funciones, clases, comentarios).
- **Idioma de la documentación:** español.
- **Tipado estricto obligatorio** en ambos stacks (mypy strict / TypeScript strict).
- Todo el código debe tener tests. **Coverage mínimo: 80 %.**

## Git

- **Conventional commits** obligatorios: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `ci:`.
- El scope indica el módulo: `feat(backend): add book search endpoint`, `fix(frontend): fix login redirect`.
- Una rama por feature: `feature/nombre-corto`.
- Los PRs van contra `main`, siempre con los tests en verde.

## Docker

- `infra/docker-compose.yml` levanta el entorno completo.
- Servicios: PostgreSQL 16, backend FastAPI, frontend React (dev), Prometheus y Grafana.
- Dockerfiles multi-stage en cada subdirectorio (`backend/Dockerfile`, `frontend/Dockerfile`).

## Configuración y secretos

- Variables de entorno en `.env` (no versionado).
- `.env.example` versionado con todas las variables necesarias y valores de ejemplo.
- Nunca se hardcodean secrets, URLs de base de datos, API keys ni tokens en el código.

## CI/CD

- GitHub Actions en `.github/workflows/`.
- Pipeline: `lint → test-backend → test-frontend → test-e2e → build → security-scan`.
- SonarQube como *quality gate* en los PRs.

## Despliegue

El frontend y el backend se desarrollan juntos en este repositorio pero se **despliegan de forma independiente**, de modo que cada parte puede escalar y publicarse según su propio calendario.
