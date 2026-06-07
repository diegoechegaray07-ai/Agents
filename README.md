# Agents — Skills portables para cualquier IA

Colección de **skills** (instrucciones especializadas + scripts) para automatizar
tareas de contabilidad y del negocio (Pets Company / DCG). Cada skill está escrita
en **markdown estándar**, así que sirve igual en Claude, GPT, Gemini, Cursor,
Codex/Coder y cualquier asistente que acepte instrucciones.

> 📖 Cómo cargarlas en cada plataforma: ver [docs/guides/usar-con-cualquier-ia.md](docs/guides/usar-con-cualquier-ia.md).
> Índice legible por máquinas (Codex/Cursor): [AGENTS.md](AGENTS.md).

## Cómo funciona el formato

Cada skill es una carpeta en [skills/](skills/) con:

```
<skill>/
├── SKILL.md      # frontmatter (name, description) + instrucciones en markdown
├── scripts/      # (opcional) código ejecutable para el trabajo determinista
└── references/   # (opcional) detalles que se leen solo cuando hacen falta
```

El `SKILL.md` es el corazón: el **cuerpo** son instrucciones en markdown puro que
podés pegar como *system prompt* en cualquier IA. El **frontmatter** (`name` /
`description`) es metadata que Claude y Cursor usan para activar la skill sola, y
que el resto de las herramientas simplemente ignora.

## Skills incluidas

### Negocio y contabilidad
| Skill | Qué hace | Requiere |
|---|---|---|
| [alegra-api](skills/alegra-api/) | Consulta ventas, facturas y medios de pago desde la API de Alegra | API + credenciales |
| [arca-informe](skills/arca-informe/) | Informe PDF de "Comprobantes Emitidos" de ARCA desde un xlsx | script Python |
| [ddjj-iibb-san-juan](skills/ddjj-iibb-san-juan/) | Liquidación de IIBB San Juan (PDF) desde un xlsx de ARCA | script Python |
| [cargar-factura-proveedor](skills/cargar-factura-proveedor/) | Lee facturas de proveedor (PDF o foto) y las carga en Alegra | OCR + API |
| [getnet-flujo-completo](skills/getnet-flujo-completo/) | Descarga transacciones de Getnet por browser + genera informe | MCP browser |
| [getnet-informe](skills/getnet-informe/) | Informe PDF de ventas Getnet desde un xlsx | script Python |
| [reposicion-stock](skills/reposicion-stock/) | Qué comprar/fraccionar cruzando stock de Alegra con ventas | script Python + API |
| [qr-pets-company](skills/qr-pets-company/) | Regenera carteles/stickers de cobro con QR de Mercado Pago | script Python |
| [marketing-ideas](skills/marketing-ideas/) | Prioriza ideas de marketing con un score de viabilidad (MFS) | solo prompt ✅ |

### Utilidades
| Skill | Qué hace | Requiere |
|---|---|---|
| [arquitecto-de-skills](skills/arquitecto-de-skills/) | Crea y optimiza skills (tokens, precisión, velocidad) | solo prompt ✅ |
| [especialista-imagenes](skills/especialista-imagenes/) | Crea, edita y compone imágenes y gráfica de marketing | scripts / Canva / API |

### Oficiales de Anthropic (documentos e infraestructura)
`docx` · `pdf` · `pptx` · `xlsx` · `skill-creator` · `schedule` · `setup-cowork`
· `consolidate-memory` · `backup-skills`.
Manipulación de documentos Office/PDF y utilidades del entorno. Incluidas como
referencia; se mantienen aparte porque son de Anthropic.

> ✅ = portable a cualquier IA sin tooling extra. Las demás necesitan ejecutar
> Python, OCR, un browser por MCP o llamar a una API.

## Credenciales

**Ninguna credencial está en este repo.** Skills como `alegra-api` leen sus
tokens de un `.env` local (no versionado). Configurá el tuyo siguiendo la guía
de cada skill.

## Estructura del repo

```
skills/      # las skills (contenido principal)
docs/        # guías de uso
src/ tests/  # andamiaje para código de agentes a futuro
AGENTS.md    # índice legible por Codex/Cursor/Coder
```

## Licencia

MIT — ver [LICENSE](LICENSE). Las skills bajo "Oficiales de Anthropic" pertenecen
a sus autores originales.
