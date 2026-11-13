# ADR-0003: Agente `migration-helper` para las migraciones de Alembic

- **Estado:** Aceptado
- **Fecha:** 2026-11-13
- **Issue / PR:** #15

## Contexto

Las migraciones se autogeneran con Alembic a partir de los modelos ORM, pero el resultado es solo un
punto de partida: `docs/backend-database-sqlalchemy.md` exige revisarlo antes de aplicarlo (nombres
de FK y de restricciones, índices en las FK, `server_default` al añadir columnas `NOT NULL` a tablas
con datos). Ya hubo que reconciliar a mano la migración de `books`. La issue #15 pide un subagente
que automatice este paso y enseñe el SQL antes de aplicarlo.

## Decisión

Creamos el subagente `migration-helper` (`.claude/agents/migration-helper.md`, modelo `sonnet`) con
solo las herramientas `Read`, `Grep` y `Bash`, y dos modos que nunca se mezclan en la misma
ejecución:

- **Generar** (por defecto): comprueba que hay una sola *head* y que la base de datos está al día,
  detecta los cambios con `alembic check`, genera la revisión con `--autogenerate`, la normaliza con
  Ruff y mypy, la revisa contra las reglas del proyecto y enseña el SQL de subida y de bajada en modo
  offline. Después se detiene.
- **Aplicar**: solo cuando el prompt dice que el SQL está aprobado y nombra la revisión. Ejecuta
  `alembic upgrade head` y verifica el resultado.

Sin herramientas de edición, el agente no retoca migraciones a mano: si hay que cambiar algo, indica
la edición exacta y la hace quien lo invoca.

## Alternativas consideradas

- **Que `fastapi-expert` genere y aplique las migraciones** — mezcla implementar con tocar la base
  de datos y no deja un punto de parada para revisar el SQL.
- **Un solo modo que genere y aplique seguido** — un subagente no puede pedir aprobación a mitad de
  ejecución, así que el SQL se aplicaría sin que nadie lo revisara.
- **Darle `Write`/`Edit` para corregir la migración** — más rápido, pero acaba reescribiendo la
  migración sin que nadie lo vea. Se prefiere que proponga el cambio y otro lo haga.

## Consecuencias

- **Positivas:** toda migración pasa por la misma lista de comprobación y su SQL se revisa antes de
  tocar la base de datos; el agente no puede cambiar el estado de Alembic con `stamp` ni
  `downgrade`.
- **Negativas / costes:** dos invocaciones por migración (generar y aplicar), y las correcciones las
  hace otro agente o la sesión principal.
- **Seguimiento:** el seed (`db-seeder`) todavía no rellena `publisher`, y el frontend tampoco
  muestra ni edita el campo.
