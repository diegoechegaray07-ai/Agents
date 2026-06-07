# Instrucciones para GitHub Copilot

Este repo es una colección de **skills**: instrucciones especializadas (más
scripts) para automatizar tareas de contabilidad y del negocio Pets Company / DCG.

Cuando la petición del usuario coincida con el alcance de una skill, **abrí y
seguí su `SKILL.md`** (cada uno trae sus scripts y referencias). No reimplementes
la lógica: el `SKILL.md` es la fuente de verdad.

## Skills disponibles

| Skill | Usar cuando el usuario… | Instrucciones |
|---|---|---|
| alegra-api | pregunte por ventas/facturas/medios de pago de Pets Company | `skills/alegra-api/SKILL.md` |
| arca-informe | suba un xlsx de ARCA y pida un informe de comprobantes | `skills/arca-informe/SKILL.md` |
| ddjj-iibb-san-juan | pida liquidar Ingresos Brutos de San Juan desde un xlsx de ARCA | `skills/ddjj-iibb-san-juan/SKILL.md` |
| cargar-factura-proveedor | suba una factura de proveedor (PDF o foto) para Alegra | `skills/cargar-factura-proveedor/SKILL.md` |
| getnet-flujo-completo | pida descargar transacciones de Getnet y/o el informe | `skills/getnet-flujo-completo/SKILL.md` |
| getnet-informe | suba un xlsx de Getnet y pida el informe de ventas | `skills/getnet-informe/SKILL.md` |
| reposicion-stock | pregunte qué comprar / reponer / análisis de stock | `skills/reposicion-stock/SKILL.md` |
| qr-pets-company | pida rehacer los carteles/QR de cobro de Pets Company | `skills/qr-pets-company/SKILL.md` |
| marketing-ideas | pida ideas/estrategia de marketing priorizadas | `skills/marketing-ideas/SKILL.md` |
| arquitecto-de-skills | quiera crear u optimizar una skill | `skills/arquitecto-de-skills/SKILL.md` |
| especialista-imagenes | quiera crear, editar o componer imágenes/gráfica | `skills/especialista-imagenes/SKILL.md` |
| docx / pdf / pptx / xlsx | trabaje con documentos Office o PDF | `skills/<tipo>/SKILL.md` |

El índice completo (incluidas las skills oficiales de Anthropic) está en
[`AGENTS.md`](../AGENTS.md).

## Reglas del repo

- **Nunca** pongas credenciales en el código. Las skills que llaman a APIs leen un
  `.env` local que no se versiona.
- Las skills con `scripts/` esperan poder ejecutar Python (`pandas`, `openpyxl`,
  `reportlab`, etc.).
- `marketing-ideas` y `arquitecto-de-skills` son solo-prompt: no necesitan tooling.
