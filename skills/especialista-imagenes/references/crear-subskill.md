# Cristalizar un flujo recurrente en una sub-skill

Cuando un pedido de imágenes se repite con parámetros estables (ej. "las placas
de Instagram del negocio X siempre con este formato, logo y paleta"), conviene
darle su propia skill en vez de rehacer la composición cada vez. Así el flujo
queda reproducible y dispara solo.

## Cómo hacerlo

**No improvises la estructura.** Delegá en la skill **arquitecto-de-skills**, que
diseña skills eficientes en tokens (carga progresiva, `description` que dispara
bien, trabajo determinista en `scripts/`). Invocala con `Skill` y pasale:

- Qué produce la sub-skill (entregables y formatos exactos).
- Con qué disparadores (frases reales que diría Diego).
- Los parámetros fijos (tamaños, paleta, fuentes, logo) y los variables.
- Que el trabajo de imagen se apoye en `imgtool.py` de esta skill o en un script
  propio del proyecto, siguiendo los patrones de [marketing.md](marketing.md).

## Cuándo conviene (y cuándo no)

| Crear sub-skill | Resolver acá nomás |
|---|---|
| Se repite y tiene parámetros estables | Pedido único o exploratorio |
| Entregables y marca definidos | Diseño todavía en tanteo |
| Diego va a pedirlo seguido | "probemos cómo queda" |

Modelo de referencia ya existente: la skill `qr-pets-company` es exactamente este
patrón (composición de gráfica de marca parametrizada por script).
