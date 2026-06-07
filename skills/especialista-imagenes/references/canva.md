# Canva (conector MCP)

Usalo cuando la tarea pide **plantillas profesionales, identidad de marca
(brand kit), o exportar a PDF/PPT/PNG de alta calidad** — cosas que el motor
local no da con la misma terminación. Las herramientas son `mcp__claude_ai_Canva__*`.

## Flujo típico

1. **Entender qué hay**: `list-brand-kits` (marcas/colores/fuentes del usuario),
   `search-designs` o `search-folders` para reusar diseños existentes.
2. **Crear**:
   - `generate-design` / `generate-design-structured` — diseño nuevo a partir de
     un prompt (poster, post, presentación). El structured permite controlar
     páginas/elementos.
   - `create-design-from-brand-template` — partir de una plantilla de marca.
   - `import-design-from-url` / `upload-asset-from-url` — traer imágenes propias
     (ej. una salida de `imgtool.py` subida a una URL) al diseño.
3. **Editar** (transaccional): `start-editing-transaction` →
   `perform-editing-operations` (varias) → `commit-editing-transaction`
   (o `cancel-editing-transaction` para abortar). Revisá con `get-design-content`
   / `get-design-pages` / `get-design-thumbnail` entre medio.
4. **Exportar**: `get-export-formats` y luego `export-design` (PNG/PDF/PPT).
   Mostrale el resultado a Diego.

## Cuándo NO usar Canva

- Retoque mecánico (resize, formato, compresión, marca de agua simple): hacelo
  local, es más rápido y no depende de la nube.
- Cuando Diego quiere control pixel-perfect y reproducible por código.

## Notas

- Confirmá con Diego antes de crear/modificar diseños en su cuenta (son cambios
  externos persistentes).
- Los nombres exactos de herramientas y sus argumentos los cargás vía
  `ToolSearch` (ej. `select:mcp__claude_ai_Canva__generate-design`) cuando vayas
  a invocarlas.
