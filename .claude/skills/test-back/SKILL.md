---
name: test-back
description: Escribe y ejecuta tests del backend (pytest). Decide si toca test unitario, de integración o de API según la capa hexagonal modificada, escribe los tests siguiendo AAA y verifica coverage mínimo del 80%. Usar tras implementar o modificar código en backend/, o cuando el usuario pida tests para el backend.
---

# Tests del backend

Escribe tests para el código de `backend/` siguiendo las convenciones del proyecto y verifica que la suite pasa con coverage ≥ 80%.

## Paso 1 — Identificar qué se testea

Determina qué archivos de `backend/src/` son el objetivo: los modificados en la conversación actual, los indicados por el usuario, o (si no hay contexto) los cambiados según `git diff` / `git status`.

## Paso 2 — Decidir el tipo de test según la capa

El tipo de test se deriva de la capa hexagonal. Un mismo cambio puede requerir tests en más de una capa:

| Capa modificada | Tipo de test | Ubicación | Estrategia |
|---|---|---|---|
| `domain/services/`, `domain/models/` | Unitario | `tests/unit/` | Mockear los ports (Protocol classes). Sin DB, sin FastAPI, sin I/O. |
| `adapters/outbound/persistence/` | Integración | `tests/integration/` | DB real de test (fixture de `conftest.py`). Verificar el repositorio contra PostgreSQL. |
| `adapters/inbound/api/` (routers, schemas, middleware) | API | `tests/api/` | `httpx.AsyncClient` contra la app FastAPI. Verificar status codes, formato `{"success", "data", "error"}` y validación de schemas. |

Reglas de decisión:

- Un endpoint nuevo normalmente necesita **dos** tests: unitario para la lógica del servicio de dominio + API para el router. El router no lleva lógica, así que su test cubre wiring, validación y traducción de errores (404, 401, 422).
- Un repositorio nuevo necesita test de **integración**; no mockees SQLAlchemy en un test unitario para "cubrir" un repositorio.
- Las excepciones de dominio se testean en unitario (que el servicio las lanza) y en API (que el middleware las traduce al HTTP status correcto).
- `config/` y `main.py` no necesitan tests dedicados salvo lógica propia.

## Paso 3 — Escribir los tests

- Patrón AAA con comentarios explícitos `# Arrange`, `# Act`, `# Assert`.
- Reutilizar fixtures de `tests/conftest.py` (test DB, async client, usuarios customer/seller autenticados). Si falta una fixture claramente reutilizable, añadirla a `conftest.py`, no duplicarla en el archivo de test.
- `pytest-asyncio` para todo lo async.
- Nombres descriptivos: `test_<funcion>_<escenario>_<resultado>` (ej. `test_find_by_id_when_book_missing_returns_none`).
- Código e identificadores en inglés. Type hints obligatorios (mypy strict también aplica a tests).
- Cubrir el camino feliz, los casos de error de dominio y los bordes de validación — no solo el happy path.

## Paso 4 — Ejecutar y verificar

Desde `backend/`:

```
pytest --cov=src --cov-report=term-missing
```

- Si hay fallos: diagnosticar y corregir (el test si está mal planteado, el código si el test revela un bug — en ese caso avisar al usuario del bug encontrado).
- Si el coverage de los módulos tocados baja del 80%: añadir casos para las líneas sin cubrir que muestra `term-missing`, priorizando ramas de error.
- Los tests de integración/API requieren la DB de test levantada; si falla la conexión, levantar el entorno con `make dev` (desde la raíz) antes de reintentar.

## Paso 5 — Reportar

Resumir al usuario: tests añadidos por tipo, resultado de la suite y coverage final en modo tabla que es más visual. Si se dejó algo sin cubrir deliberadamente, decirlo explícitamente.
