# ADR-0002: Agente `test-writer` separado para los tests del backend

- **Estado:** Aceptado
- **Fecha:** 2026-11-13

## Contexto

El backend tiene un subagente de implementación (`fastapi-expert`) y una skill con el procedimiento
para escribir tests (`test-back`). Había que decidir quién escribe los tests de un cambio:

1. que `fastapi-expert` cargue la skill `test-back` y teste su propio código, o
2. un subagente distinto que la cargue y se dedique solo a los tests.

Los subagentes no heredan las skills de la sesión principal: para que un subagente use `test-back`
hay que precargarla con el campo `skills:` de su frontmatter.

## Decisión

Creamos el subagente `test-writer` (`.claude/agents/test-writer.md`), que precarga `test-back` y
solo escribe dentro de `backend/tests/`. El flujo para un cambio de backend es:

`fastapi-expert` implementa → `test-writer` escribe y ejecuta los tests en la misma rama →
`code-reviewer` revisa.

Si un test destapa un bug, `test-writer` no toca el código de producción: deja el test fallando como
evidencia e informa del bug.

## Alternativas consideradas

- **`fastapi-expert` con `skills: [test-back]`** — una sola ejecución y más barata, pero los tests
  salen de la misma cabeza que el código: comparten sus puntos ciegos y el agente tiende a corregir
  en silencio sus propios fallos.
- **Implementación y tests en paralelo, en dos worktrees** — el worktree de tests no ve el código
  hasta que se hace merge, y `test-back`, sin más contexto, localiza el cambio con `git diff`.
  Además, los tests de integración usan un contenedor con nombre y puerto fijos
  (`backend/tests/integration/conftest.py`), así que dos ejecuciones simultáneas chocan. Los
  worktrees quedan para trabajar en *features distintas* en paralelo.

## Consecuencias

- **Positivas:** los tests se derivan del comportamiento esperado (issue, puertos, esquemas) y no
  del código; los prompts son más pequeños y enfocados; los bugs quedan a la vista en lugar de
  arreglarse en silencio.
- **Negativas / costes:** dos ejecuciones de agente por cambio en lugar de una.
- **Seguimiento:**
  - `fastapi-expert` mantiene su sección «Testing Guidelines»; conviene que delegue los tests en
    `test-writer`.
  - Por ahora solo cubre el backend; para el frontend haría falta una skill `test-front`.
  - Para lanzar tests en varios worktrees a la vez, el contenedor de integración necesita un nombre
    y un puerto únicos por worktree.
