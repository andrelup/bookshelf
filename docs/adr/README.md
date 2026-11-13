# Registro de decisiones de arquitectura (ADR)

Esta carpeta recoge las decisiones relevantes que tomamos a lo largo del curso: de arquitectura, de
herramientas, de flujo de trabajo y de configuración de agentes. Cada ADR explica **qué** se
decidió, **por qué** y **qué consecuencias** tiene, para que cualquiera (o un agente que empieza sin
contexto) entienda el motivo sin tener que reconstruirlo.

## Cuándo escribir un ADR

Escribe uno cuando la decisión:

- afecte a la estructura del código o a cómo se comunican las piezas (capas, puertos, librerías,
  base de datos);
- cambie el flujo de trabajo o las herramientas (CI, hooks, agentes, skills, convenciones);
- descarte alternativas razonables que alguien podría volver a proponer;
- sea cara de revertir.

No hace falta para cambios rutinarios que ya cubren las guías de `docs/`.

## Cómo crear uno

1. Copia [`template.md`](./template.md) como `NNNN-titulo-en-kebab-case.md`, con el siguiente
   número libre (cuatro dígitos).
2. Rellénalo con estado **Propuesto** y pásalo a **Aceptado** cuando se apruebe (o al hacer merge
   del PR que lo introduce).
3. Añade una fila al índice de abajo.
4. Un ADR aceptado no se reescribe: si la decisión cambia, crea un ADR nuevo que lo **sustituya** y
   marca el antiguo como `Sustituido por ADR-NNNN`.

## Estados

| Estado | Significado |
|---|---|
| Propuesto | En discusión; todavía no aplica. |
| Aceptado | Vigente. |
| Rechazado | Se valoró y se descartó; se guarda para no repetir el debate. |
| Obsoleto | Ya no aplica y no tiene sustituto. |
| Sustituido por ADR-NNNN | Reemplazado por otra decisión. |

## Índice

| ADR | Título | Estado | Fecha |
|---|---|---|---|
| [0001](./0001-registrar-decisiones-de-arquitectura.md) | Registrar las decisiones de arquitectura con ADR | Aceptado | 2026-11-13 |
| [0002](./0002-agente-test-writer-separado.md) | Agente `test-writer` separado para los tests del backend | Aceptado | 2026-11-13 |
