# Medir una skill (tokens, tiempo, triggering)

Leé esto solo si Diego quiere rigor cuantitativo. Para la mayoría de los casos,
una revisión cualitativa con el checklist alcanza.

## Medir tokens y tiempo (con vs. sin skill)

La idea: correr la misma tarea dos veces —una con la skill, otra sin ella— y
comparar tokens consumidos y duración. La diferencia te dice si la skill
realmente ayuda o solo agrega peso.

1. Definí 2-3 prompts de prueba realistas (lo que Diego escribiría de verdad).
2. Para cada prompt, corré dos veces: una con acceso a la skill, otra sin (baseline).
3. Anotá por corrida: `total_tokens`, `duration_ms`, y si el resultado fue correcto.
4. Compará. Una buena skill baja tokens/tiempo **o** sube la precisión sin inflar
   demasiado el contexto. Si la versión con skill es más lenta y no más precisa,
   la skill está de más o está inflada.

Plantilla por corrida:

```json
{ "prompt": "...", "con_skill": true, "total_tokens": 0, "duration_ms": 0, "correcto": true }
```

## Medir triggering (¿dispara cuando debe?)

El `description` decide si la skill se activa. Para evaluarlo:

1. Armá ~15-20 queries: mitad que **deberían** disparar, mitad que **no**.
2. Las negativas valiosas son las "casi": comparten palabras con la skill pero
   necesitan otra cosa. (Una negativa obvia no prueba nada.)
3. Las positivas: distintos fraseos del mismo intento, casos donde el usuario no
   nombra la skill, y casos donde compite con otra skill pero debería ganar.
4. Corré cada query y mirá si disparó. Ajustá la `description` y repetí.

```json
[
  { "query": "...", "deberia_disparar": true },
  { "query": "...", "deberia_disparar": false }
]
```

## Nota sobre el triggering

Claude solo consulta skills para tareas que no resuelve trivialmente solo. Un
"leé este PDF" puede no disparar aunque la descripción matchee, porque lo hace
directo. Por eso los queries de prueba tienen que ser sustanciales —
multi-paso o especializados— para que el triggering sea representativo.
