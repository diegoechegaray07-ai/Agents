# Checklist de auditoría de una skill

Leé esto cuando te pidan optimizar/auditar una skill existente. Recorré el
`SKILL.md` y los recursos con esta lista; por cada punto marcá si pasa o qué
corregir.

## Metadata (nivel siempre-cargado)

- [ ] La `description` dice **qué hace** Y **cuándo usarla** con frases concretas.
- [ ] No es genérica (no dispararía de más) ni demasiado angosta (no sub-dispara).
- [ ] El "cuándo usar" está **solo** acá, no repetido en el cuerpo.
- [ ] Incluye variantes de fraseo reales del usuario (formal, casual, sin nombrar la skill).

## Cuerpo (nivel se-carga-al-disparar)

- [ ] Menos de 500 líneas; idealmente < 200. Si pasa, falta jerarquía/recursos.
- [ ] No hay prosa describiendo trabajo determinista que debería ser un script.
- [ ] No hay instrucciones de casos de borde que deberían estar en `references/`.
- [ ] Ningún dato aparece dos veces (alícuotas, rutas, formatos, nombres de columna).
- [ ] Estilo imperativo; sin relleno, sin intros, sin disclaimers obvios.
- [ ] Los `SIEMPRE`/`NUNCA` están justificados con el porqué (o reescritos).
- [ ] Datos estructurados en tablas/listas, no en párrafos largos.

## Recursos (nivel bajo-demanda)

- [ ] Cada `references/*.md` está referenciado desde el cuerpo con *cuándo* leerlo.
- [ ] Archivos de referencia > 300 líneas tienen índice (tabla de contenidos).
- [ ] El trabajo repetitivo/determinista vive en `scripts/`, no en prosa.
- [ ] Un mismo helper que se usaría en varios casos está bundleado una sola vez.
- [ ] Los `assets/` (plantillas, fuentes) no están embebidos como texto en el cuerpo.

## Velocidad / precisión

- [ ] El flujo principal no obliga a leer archivos que no se necesitan siempre.
- [ ] No hay pasos que el modelo termine salteando o que lo hagan dar vueltas
      (revisá transcripts si hay dudas: si pierde tiempo, recortá lo que lo causa).
- [ ] El cuerpo se sostiene solo: alguien que solo lee el SKILL.md puede ejecutar el flujo.

## Salida del informe

Reportá en este formato:

```
Skill: <nombre>  ·  Antes: <N> líneas  →  Después: <M> líneas

Recortes (mover/borrar):
- ...

A scripts/:
- ...

A references/:
- ...

description nueva:
- antes: "..."
- después: "..."
```
