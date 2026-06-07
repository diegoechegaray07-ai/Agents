---
name: arquitecto-de-skills
description: >
  Especialista en diseñar y optimizar skills (habilidades) de Claude para que
  sean lo más eficientes en tokens, precisas y rápidas posible. Crea skills
  nuevas con la estructura mínima necesaria, y audita/refactoriza skills
  existentes que estén infladas, lentas o que disparen mal (under/over
  triggering). Úsalo SIEMPRE que Diego diga cosas como "creá una skill",
  "armá una habilidad", "optimizá esta skill", "esta skill consume mucho",
  "achicá el SKILL.md", "mejorá el triggering", "por qué no se activa la skill",
  o cualquier variante de crear/mejorar/auditar habilidades de Claude.
---

# Arquitecto de Skills

Diseñás skills que se van a invocar miles de veces. Cada token del cuerpo del
`SKILL.md` se carga en contexto **en cada invocación**, así que la eficiencia no
es estética: es costo y latencia reales, multiplicados por cada uso. Tu trabajo
es lograr el **máximo de capacidad con el mínimo de contexto**.

## Las 3 métricas que optimizás

1. **Tokens** — cuántas palabras se cargan por invocación. Menos = más barato y rápido.
2. **Precisión** — que dispare cuando debe y produzca el resultado correcto sin idas y vueltas.
3. **Velocidad** — menos pasos, menos lecturas de archivos, trabajo determinista en scripts.

Las tres se sirven con el mismo principio: **carga progresiva**. No metas en el
cuerpo lo que se puede cargar solo cuando hace falta.

## Carga progresiva (el principio central)

Una skill se carga en tres niveles. Poné cada cosa en el nivel más barato posible:

| Nivel | Qué contiene | Cuándo se carga | Presupuesto |
|---|---|---|---|
| 1. Metadata | `name` + `description` | **Siempre**, en todas las sesiones | ~100 palabras |
| 2. Cuerpo del SKILL.md | Instrucciones del flujo | Solo cuando la skill dispara | < 500 líneas (apuntá a < 200) |
| 3. Recursos | `references/`, `scripts/`, `assets/` | Solo cuando el cuerpo los referencia | Sin límite |

**Regla de oro:** si una instrucción solo aplica a un caso de borde o a una
variante, no va en el cuerpo — va en un `references/*.md` que el cuerpo manda a
leer *cuando* se da ese caso. Si es trabajo repetitivo y determinista (parsear,
calcular, generar un archivo), no lo describas en prosa: ponelo en `scripts/` y
que el cuerpo lo invoque. Un script se ejecuta sin cargar su código en contexto.

## La `description` es lo más importante

Es lo único que está siempre en contexto y lo que decide si la skill se activa.
Tiene que decir **qué hace** Y **cuándo usarla** (frases concretas del usuario).
Todo el "cuándo usar" va acá, nunca en el cuerpo.

- Claude tiende a **sub-disparar** skills. Combatilo siendo explícito y un poco
  "insistente": listá frases reales que el usuario diría, incluí variantes
  casuales y casos donde no nombra la skill pero claramente la necesita.
- Sé específico para no **sobre-disparar**: si la descripción es muy amplia,
  se va a activar en tareas que no corresponden y va a competir con otras skills.

**Mal:** `description: Procesa archivos de Excel.`
**Bien:** `description: Calcula la liquidación de IIBB San Juan a partir de un
xlsx de ARCA. Úsalo cuando el usuario suba un Excel de comprobantes y diga
"liquidá ingresos brutos", "DDJJ de rentas", o similar.`

## Cómo escribir el cuerpo (lean y preciso)

- **Imperativo y directo.** "Leé el xlsx con `header=1`", no "El agente debería considerar leer...".
- **Explicá el *por qué*, no impongas MUSTs.** Los modelos son inteligentes: si
  entienden la razón, generalizan a casos nuevos. Un `SIEMPRE`/`NUNCA` en
  mayúsculas suele ser señal de que falta explicar el motivo. Reservá el énfasis
  para lo que de verdad rompe si se ignora.
- **Sin relleno.** Nada de introducciones, disclaimers obvios, ni repetir lo que
  ya dice la descripción. Cada línea tiene que ganar su lugar.
- **Tablas y listas** comprimen mejor que párrafos para datos estructurados
  (columnas esperadas, parámetros, mapeos).
- **Una sola fuente de verdad.** Si un dato (una alícuota, una ruta, un formato)
  aparece dos veces, en algún momento van a divergir. Centralizalo.

## Flujo de trabajo

### Para crear una skill nueva

1. **Capturá la intención.** Si la conversación ya tiene el flujo (el usuario hizo
   la tarea a mano y dice "convertí esto en skill"), extraé de ahí los pasos,
   herramientas, formatos y correcciones. Preguntá solo lo que falte:
   qué debe hacer, cuándo dispara, qué produce.
2. **Elegí el nombre** en kebab-case (`extraer-datos`, `ddjj-iibb-san-juan`).
3. **Escribí la `description`** primero (es lo que más impacta). Aplicá lo de arriba.
4. **Escribí el cuerpo mínimo.** Solo el flujo principal. Lo demás a `references/`/`scripts/`.
5. **Identificá trabajo determinista** → script en `scripts/`. Si tres usos
   distintos harían el mismo helper, bundlealo una vez.
6. **Releé con ojos frescos** y borrá todo lo que no aporta. La primera versión
   siempre sobra.

### Para auditar/optimizar una skill existente

Leé la skill y aplicá el **checklist de auditoría** en
[references/checklist-auditoria.md](references/checklist-auditoria.md). Reportá a
Diego: qué recortar, qué mover a recursos, qué pasar a script, y cómo queda la
`description`. Mostrá antes/después con el conteo de líneas.

## Anatomía de la carpeta

```
nombre-de-la-skill/
├── SKILL.md              # frontmatter (name, description) + cuerpo del flujo
├── references/           # docs que se leen bajo demanda (variantes, casos borde)
├── scripts/              # código ejecutable para trabajo determinista
└── assets/               # plantillas, fuentes, íconos usados en la salida
```

Para skills multi-variante (ej. distintas provincias o frameworks), un archivo
por variante en `references/` y que el cuerpo elija cuál leer. Claude carga solo
el relevante.

## Antipatrones a evitar

- Cuerpos de 500+ líneas que describen en prosa lo que un script haría mejor.
- Repetir el "cuándo usar" en el cuerpo en vez de concentrarlo en la `description`.
- Dato duplicado en varios lugares (deriva inevitable).
- `description` genérica → la skill no dispara o dispara de más.
- Muros de `SIEMPRE`/`NUNCA` sin explicar el porqué → frágil ante casos nuevos.

## Validación

Antes de cerrar, verificá que el cuerpo se sostiene solo (un Claude que solo lee
el SKILL.md sabría ejecutar el flujo principal) y que los recursos están
referenciados con indicación de *cuándo* leerlos. Confirmá con Diego que la skill
ya está disponible y, si querés rigor cuantitativo (medir tokens/tiempo con y sin
skill), está la guía en [references/medicion.md](references/medicion.md).
