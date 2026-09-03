# Comandos unificados del monorepo BookShelf.
# Todos se ejecutan desde la raiz del repo.
#
# Primer contacto con el repo:
#   make setup      deja el entorno local listo para trabajar (una sola vez)
#   make dev-back   API con hot reload  (terminal 1)
#   make dev-front  SPA con hot reload  (terminal 2)
#
# Los targets no necesitan que el entorno virtual este activado: llaman al
# interprete de .venv por ruta. Windows y Linux/macOS colocan los binarios
# del venv en carpetas distintas, de ahi la deteccion de abajo.
#
# Ningun target hace `cd backend`: todo se invoca desde la raiz, igual que
# pre-commit. Si no, mypy y pytest dejan un segundo juego de cachees dentro de
# backend/, porque las escriben en su cwd. Por eso se les pasa la config por
# ruta. ruff es la excepcion: no mira el cwd sino el pyproject.toml que
# descubre, asi que ademas necesita --cache-dir para no crear backend/.ruff_cache.
#
# Los `echo` van sin parentesis ni comillas a proposito, y las rutas del venv
# con barras normales: make usa sh.exe si esta en el PATH (Git Bash) y cmd.exe
# si no. sh se come los backslashes y falla con los metacaracteres; el texto
# plano y las barras normales funcionan en los dos.

ifeq ($(OS),Windows_NT)
SYS_PYTHON ?= python
PYTHON := .venv/Scripts/python.exe
else
SYS_PYTHON ?= python3
PYTHON := .venv/bin/python
endif

# Argumentos extra para `make setup`, p. ej.:
#   make setup ARGS="--skip-db"
ARGS ?=

.DEFAULT_GOAL := help

.PHONY: help setup install-hooks dev dev-back dev-front db-up db-down db-logs \
        test test-back test-front test-e2e lint lint-front format-front \
        migrate seed build

## help: lista los comandos disponibles.
help:
	@echo BookShelf - comandos disponibles
	@echo   make setup - deja el entorno local listo para trabajar
	@echo   make dev-back - backend con hot reload en el host, puerto 8000
	@echo   make dev-front - frontend con hot reload en el host, puerto 3000
	@echo   make dev - todo el entorno en Docker Compose
	@echo   make db-up - solo PostgreSQL en Docker, en background
	@echo   make db-down - para los contenedores de infra
	@echo   make db-logs - logs de PostgreSQL
	@echo   make migrate - alembic upgrade head
	@echo   make seed - datos de ejemplo en la base de datos
	@echo   make test - tests de backend + frontend
	@echo   make test-back - solo tests del backend
	@echo   make test-front - solo tests del frontend
	@echo   make test-e2e - tests end-to-end
	@echo   make lint - ruff + mypy + eslint
	@echo   make lint-front - solo eslint
	@echo   make format-front - reescribe el frontend con Prettier
	@echo   make install-hooks - solo los hooks de git
	@echo   make build - imagenes Docker de backend y frontend

## setup: getting started completo. Idempotente, se puede relanzar sin miedo.
## Crea el .env, el entorno virtual, instala backend + frontend + hooks de
## pre-commit, levanta PostgreSQL y aplica migraciones y datos de ejemplo.
## Al terminar solo hace falta `make dev-back` y `make dev-front`.
setup:
	$(SYS_PYTHON) scripts/setup.py $(ARGS)

## install-hooks: solo la parte de hooks de `make setup`. Instala las
## dependencias npm del frontend (los hooks usan el ESLint/Prettier de
## frontend/node_modules) y engancha pre-commit en .git/hooks/pre-commit.
install-hooks:
	npm --prefix frontend ci
	$(PYTHON) -m pre_commit install

## dev: levanta todo el entorno (PostgreSQL + backend con hot reload) via
## Docker Compose. No requiere nada instalado en local, pero para desarrollar
## a diario es mas comodo `make dev-back` + `make dev-front`.
dev:
	cd infra && docker compose --env-file ../.env up --build

## dev-back: backend en el host con hot reload, contra la PostgreSQL de Docker.
## Requiere `make setup` (o al menos `make db-up`) hecho antes.
dev-back:
	$(PYTHON) -m uvicorn src.main:app --reload --reload-dir backend/src --port 8000

## dev-front: frontend en el host con hot reload (Vite, puerto 3000).
dev-front:
	npm --prefix frontend run dev

## db-up: levanta solo PostgreSQL en background (lo que necesita `make dev-back`).
db-up:
	cd infra && docker compose --env-file ../.env up -d postgres

## db-down: para y elimina los contenedores de infra (los datos sobreviven en
## el volumen postgres_data).
db-down:
	cd infra && docker compose --env-file ../.env down

## db-logs: sigue los logs de PostgreSQL.
db-logs:
	cd infra && docker compose --env-file ../.env logs -f postgres

## test: suite completa. Por ahora solo hay tests de backend cableados;
## test-front/test-e2e se activaran en tareas futuras.
test: test-back

## test-back: tests del backend (pytest) con reporte de cobertura.
test-back:
	$(PYTHON) -m pytest backend -c backend/pyproject.toml -o cache_dir=../.pytest_cache --cov=backend/src --cov-report=term-missing

## test-front: placeholder hasta que el frontend tenga suite de tests
## configurada (ver issue futura). No debe romper `make test`.
test-front:
	@echo test-front: aun no hay suite de tests configurada en frontend - pendiente

## test-e2e: placeholder hasta que se configure Playwright.
test-e2e:
	@echo test-e2e: aun no hay tests end-to-end configurados - pendiente

## lint: ruff check + mypy en backend, eslint en frontend.
lint:
	$(PYTHON) -m ruff check --cache-dir .ruff_cache backend
	$(PYTHON) -m mypy --config-file backend/pyproject.toml backend
	npm --prefix frontend run lint

## lint-front: solo el linter del frontend (eslint, falla con cualquier warning).
lint-front:
	npm --prefix frontend run lint

## format-front: reescribe el frontend con el formato de Prettier.
format-front:
	npm --prefix frontend run format

## migrate: aplica las migraciones de Alembic hasta la ultima revision.
migrate:
	$(PYTHON) -m alembic -c backend/alembic.ini upgrade head

## seed: pobla la base de datos con datos de ejemplo.
seed:
	$(PYTHON) backend/seed.py

## build: construye las imagenes Docker de backend y frontend.
## frontend/Dockerfile aun no existe (llegara en una tarea futura); mientras
## tanto este target solo construye la imagen de backend sin romper `make`.
build:
	docker build -t bookshelf-backend ./backend
ifeq ($(wildcard frontend/Dockerfile),)
	@echo build: frontend/Dockerfile aun no existe - pendiente
else
	docker build -t bookshelf-frontend ./frontend
endif
