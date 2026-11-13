# ADR-0001: Registrar las decisiones de arquitectura con ADR

- **Estado:** Aceptado
- **Fecha:** 2026-11-13

## Contexto

BookShelf es un proyecto de formación que crece por iteraciones a lo largo del curso. Muchas
decisiones (arquitectura hexagonal, Bulletproof React, cómo se lanzan los tests de integración, qué
agente hace qué) se toman en conversación y solo quedan reflejadas en el código o en un mensaje de
commit. Con el tiempo, ni nosotros ni los agentes, que empiezan cada sesión sin memoria del
proyecto, sabemos por qué se hizo así ni qué alternativas se descartaron.

## Decisión

Registraremos cada decisión relevante como un *Architecture Decision Record* (ADR) en `docs/adr/`,
con el formato de Michael Nygard ampliado con un apartado de alternativas (ver
[`template.md`](./template.md)). Los ADR se numeran de forma correlativa, no se reescriben una vez
aceptados y, si la decisión cambia, se sustituyen por un ADR nuevo.

## Alternativas consideradas

- **Solo mensajes de commit y descripciones de PR** — se pierden entre cientos de commits y no
  recogen las alternativas descartadas.
- **Una sección de decisiones en `CLAUDE.md`** — se carga en todas las sesiones y engorda el
  contexto de todos los agentes con información que casi nunca necesitan.
- **Un único documento con todas las decisiones** — difícil de revisar en un PR y sin un historial
  claro por decisión.

## Consecuencias

- **Positivas:** el porqué de cada decisión queda versionado junto al código y se revisa en el
  mismo PR que la introduce.
- **Negativas / costes:** escribir un ADR lleva unos minutos por decisión.
- **Seguimiento:** el `CLAUDE.md` raíz y `docs/README.md` enlazan a esta carpeta para que los
  agentes la consulten antes de cambiar una decisión de este tipo.
