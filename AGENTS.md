# AGENTS.md

Índice de skills disponibles en este repo, en el formato estándar `AGENTS.md` que
leen Codex, Cursor, Coder y otros agentes. Cada skill es un conjunto de
instrucciones especializadas; activá la que corresponda según la tarea del usuario.

## Cómo usar este archivo

Cuando la petición del usuario coincida con el alcance de una skill, **leé su
`SKILL.md`** y seguí esas instrucciones. La columna "Activar cuando" resume el
disparador; el detalle completo está en el `description` de cada `SKILL.md`.

## Skills

| Skill | Activar cuando el usuario… | Archivo |
|---|---|---|
| alegra-api | pregunte por ventas/facturas/medios de pago de Pets Company | [skills/alegra-api/SKILL.md](skills/alegra-api/SKILL.md) |
| arca-informe | suba un xlsx de ARCA y pida un informe de comprobantes | [skills/arca-informe/SKILL.md](skills/arca-informe/SKILL.md) |
| ddjj-iibb-san-juan | pida liquidar Ingresos Brutos de San Juan desde un xlsx de ARCA | [skills/ddjj-iibb-san-juan/SKILL.md](skills/ddjj-iibb-san-juan/SKILL.md) |
| cargar-factura-proveedor | suba una factura de proveedor (PDF o foto) para cargar en Alegra | [skills/cargar-factura-proveedor/SKILL.md](skills/cargar-factura-proveedor/SKILL.md) |
| getnet *(en repo aparte)* | pida un informe de ventas Getnet (de domingo/martes/miércoles, DCG1…DCG9) | repo `GitHub/getnet` → `skills/getnet/SKILL.md` |
| reposicion-stock | pregunte qué comprar / qué reponer / análisis de stock | [skills/reposicion-stock/SKILL.md](skills/reposicion-stock/SKILL.md) |
| qr-pets-company | pida rehacer los carteles/QR de cobro de Pets Company | [skills/qr-pets-company/SKILL.md](skills/qr-pets-company/SKILL.md) |
| marketing-ideas | pida ideas/estrategia de marketing priorizadas | [skills/marketing-ideas/SKILL.md](skills/marketing-ideas/SKILL.md) |
| arquitecto-de-skills | quiera crear u optimizar una skill | [skills/arquitecto-de-skills/SKILL.md](skills/arquitecto-de-skills/SKILL.md) |
| especialista-imagenes | quiera crear, editar o componer imágenes/gráfica | [skills/especialista-imagenes/SKILL.md](skills/especialista-imagenes/SKILL.md) |
| docx / pdf / pptx / xlsx | trabaje con documentos Office o PDF | [skills/](skills/) |
| skill-creator | quiera crear y evaluar skills con tests (flujo Anthropic) | [skills/skill-creator/SKILL.md](skills/skill-creator/SKILL.md) |

## Convenciones

- **Credenciales:** nunca en el repo. Las skills que llaman a APIs leen un `.env`
  local. No pegues tokens en los archivos.
- **Scripts:** las skills con `scripts/` esperan un entorno que ejecute Python
  (con `pandas`, `openpyxl`, `reportlab`, etc. según el caso).
- **Skills solo-prompt** (sin tooling): `marketing-ideas`, `arquitecto-de-skills`.
  Funcionan en cualquier chat sin instalar nada.
