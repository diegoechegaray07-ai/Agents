# Usar estas skills con cualquier IA

Cada skill es markdown estándar, así que el contenido funciona en todas las
plataformas. Lo que cambia es **dónde** se pega o se coloca el archivo para que la
IA lo tome. Acá está el cómo, plataforma por plataforma.

La regla general: **el cuerpo del `SKILL.md`** (todo lo que está debajo del
frontmatter `---`) son las instrucciones. Eso es lo que se usa como prompt. El
frontmatter (`name`, `description`) es metadata opcional.

> ⚠️ Las skills con `scripts/` necesitan un entorno que ejecute Python (ChatGPT
> con Code Interpreter, Claude Code, Cursor, etc.). Las skills "solo-prompt"
> (`marketing-ideas`, `arquitecto-de-skills`) andan en cualquier chat sin nada extra.

---

## Claude Code (terminal / IDE)

Copiá la carpeta de la skill a tu directorio de skills y se activa sola por su
`description`:

```bash
cp -r skills/arca-informe ~/.claude/skills/        # global
# o, por proyecto:
cp -r skills/arca-informe .claude/skills/
```

Reiniciá la sesión y listo. No hace falta nombrarla: Claude la dispara cuando la
tarea coincide.

## Claude.ai (web/desktop)

Subí la skill empaquetada como `.skill` (Settings → Capabilities → Skills), o
pegá el cuerpo del `SKILL.md` al inicio de la conversación o en las instrucciones
del proyecto.

## Cursor

**Ya está listo:** el repo trae `.cursor/rules/*.mdc` (uno por skill). Al abrir el
repo en Cursor, las reglas se cargan solas y cada una apunta a su `SKILL.md`.
Cursor también respeta el `AGENTS.md` de la raíz como contexto del proyecto. No
hay que configurar nada; si querés agregar una skill nueva, copiá una `.mdc`
existente y cambiale el nombre y la `description`.

## GitHub Copilot

**Ya está listo:** el repo trae `.github/copilot-instructions.md` con el índice de
skills, que Copilot toma automáticamente en este repo. Apunta a cada `SKILL.md`
para que Copilot lo lea cuando la tarea coincida.

## OpenAI Codex / Codex CLI / "Coder" y agentes que leen AGENTS.md

Estos agentes leen el [AGENTS.md](../../AGENTS.md) de la raíz automáticamente. Con
tener el repo clonado alcanza: el agente ve el índice y abre el `SKILL.md` que
corresponda. No hay que configurar nada más.

## ChatGPT — GPT personalizado (Custom GPT)

1. Crear un GPT → pestaña **Configure**.
2. En **Instructions**, pegá el cuerpo del `SKILL.md`.
3. Si la skill tiene `scripts/`, subí esos archivos en **Knowledge** y activá
   **Code Interpreter** para que pueda ejecutarlos.

## ChatGPT / GPT (chat normal)

Pegá el cuerpo del `SKILL.md` como primer mensaje, o guardalo en "Custom
Instructions". Para skills con script, subí el `.py` al chat (Code Interpreter).

## Gemini — Gems

1. Gemini → **Gems** → crear un Gem.
2. Pegá el cuerpo del `SKILL.md` en las instrucciones del Gem.
3. Para datos/archivos, adjuntalos en el chat del Gem.

## Cualquier otro asistente

Pegá el cuerpo del `SKILL.md` como *system prompt* o primer mensaje. Es markdown,
lo entiende cualquier modelo. Si referencia un script o un `.env`, vas a necesitar
un entorno que ejecute código y las credenciales correspondientes.

---

## Qué tan portable es cada skill

| Tipo | Skills | Portabilidad |
|---|---|---|
| Solo prompt | `marketing-ideas`, `arquitecto-de-skills` | Total: cualquier chat |
| Prompt + script Python | `arca-informe`, `ddjj-iibb-san-juan`, `getnet-informe`, `reposicion-stock`, `qr-pets-company`, `docx`, `pdf`, `pptx`, `xlsx` | Necesita ejecutar Python |
| Prompt + API externa | `alegra-api`, `cargar-factura-proveedor` | Necesita API + credenciales en `.env` |
| Prompt + browser (MCP) | `getnet-flujo-completo` | Necesita un navegador controlable por la IA |
| Prompt + imágenes | `especialista-imagenes` | Mejor con tooling de imágenes/Canva |
