# Generación desde texto (IA)

Para crear pixeles que **no existen todavía** (logo, ilustración, fondo,
concepto) a partir de una descripción. Claude no genera imágenes por sí mismo;
hay que delegar en un motor generativo.

## Opciones, en orden de preferencia

1. **Canva `generate-design`** — ya disponible vía MCP, sin claves extra. Ideal
   para piezas con texto/layout (posters, placas). Ver [canva.md](canva.md).
2. **API externa de generación** (ej. modelos texto→imagen). Requiere una clave
   propia. Antes de asumir nada, preguntá a Diego qué proveedor/clave quiere usar
   y guardá la clave en variable de entorno (nunca hardcodeada).
3. Si no hay motor disponible, **decílo claro** y ofrecé alternativas (Canva, un
   banco de imágenes, o componer local a partir de assets existentes).

## Buen prompt de imagen

Estructurá: **sujeto + estilo + composición + iluminación + paleta + formato**.
Ej: "logo minimalista de una huella de perro, vector plano, dos colores
(turquesa y blanco), fondo transparente, centrado". Cuanto más concreto, menos
iteraciones.

## Flujo recomendado

1. Aclarar con Diego: uso final, dimensiones, estilo, si lleva texto.
2. Generar 2–3 variantes para elegir.
3. Pasar la elegida por el motor **local** (`imgtool.py`) para el acabado:
   recortar al aspecto exacto, quitar fondo, redimensionar, comprimir.

La generación crea el material; el retoque fino y el formato final casi siempre
conviene cerrarlos local.
