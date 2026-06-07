# Documentos visuales (diagramas, infografías, gráficos)

Elegí la herramienta según el tipo:

| Tipo | Herramienta | Por qué |
|---|---|---|
| Diagrama de flujo, arquitectura, relaciones | **Mermaid** o **Graphviz/DOT** | texto → diagrama, versionable, limpio |
| Gráfico con datos (barras, líneas, torta) | **matplotlib** (Python) | preciso, exporta PNG/SVG/PDF |
| Infografía con layout libre | **Composición local** (ver [marketing.md](marketing.md)) o **Canva** | control de diseño |
| Presentación | **Canva** (export PPT) | plantillas + export nativo |

## Gráficos con datos (matplotlib)

`matplotlib` viene con el entorno Python. Generá el gráfico, guardalo con
`savefig(ruta, dpi=200, bbox_inches="tight")`, y **borrá el archivo antes** si
existe (gotcha OneDrive). Mantené el estilo sobrio: pocos colores, etiquetas
claras, sin chartjunk.

## Diagramas (Mermaid)

Escribí el diagrama en sintaxis Mermaid. Si necesitás un PNG/SVG renderizado y no
hay extensión que lo haga, ofrecé renderizarlo con `mmdc` (mermaid-cli, requiere
Node) o entregá el bloque Mermaid para que Diego lo pegue donde lo soporten.

## Composición a partir de datos del usuario

Si Diego pasa una tabla/Excel y quiere visualizarla, primero entendé los datos,
proponé el tipo de gráfico adecuado al mensaje (comparar → barras, evolución →
líneas, proporción → torta/treemap), y recién después generá.
