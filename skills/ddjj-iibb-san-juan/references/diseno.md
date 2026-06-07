# Diseño del PDF — DDJJ IIBB San Juan

> Ya implementado en `scripts/generar_ddjj_sanjuan.py`. Leé esto solo si vas a
> **modificar** el diseño; para liquidar normalmente no hace falta.

Hereda el lenguaje visual de `arca-informe` pero con **acento verde** (`#059669`)
para distinguir de un vistazo el documento de IIBB del informe de comprobantes.
No reescribir el diseño salvo que Diego lo pida. Estructura:

- **Encabezado**: título "DDJJ Ingresos Brutos — San Juan", subtítulo
  "Régimen Local · CUIT", chips de PERÍODO / CONTRIBUYENTE / ALÍCUOTA.
- **KPIs** (4 tarjetas): Base Imponible · Alícuota · Impuesto Determinado ·
  **Saldo a Pagar** (resaltado).
- **Determinación del impuesto** (tabla): base imponible → alícuota →
  impuesto determinado.
- **Deducciones** (tabla, solo si hay alguna > 0): retenciones, percepciones,
  percepciones bancarias, saldo a favor anterior, total.
- **Resultado**: impuesto determinado − deducciones = saldo a pagar / a favor.
- **Detalle de ventas del período** (tabla): ventas por fecha con neto gravado,
  neteando notas de crédito.
- Footer con fecha de generación y aclaración "Liquidación de apoyo — verificar
  contra la presentación oficial de la DGR San Juan".
