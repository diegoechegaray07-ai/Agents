---
name: qr-pets-company
description: >-
  Regenera los materiales de cobro con QR de Pets Company: el cartel base (PNG),
  el cartel A4 (PDF) y el sticker/tarjeta (PNG y PDF), que sirven para cobrar por
  transferencia de Mercado Pago (alias petscompany, sin comisión). Opcionalmente
  regenera primero el QR oficial interoperable (Coelsa/EMVCo) a partir de un
  CVU/CBU. USAR SIEMPRE que Diego diga cosas como "rehacé/regenerá los carteles
  de Pets Company", "actualizá el QR de Pets Company", "generá de nuevo el sticker
  o el cartel A4", "cambió el CVU, rehacé el QR", o cualquier variante de
  regenerar/actualizar los materiales QR de Pets Company. También aplica si pasa
  un CVU/CBU de 22 dígitos y pide actualizar el QR de cobro.
---

# Materiales QR de Pets Company

Pets Company cobra **por transferencia de Mercado Pago** (alias `petscompany`),
no con el QR de cobro de MP (que tiene comisión). Estos materiales muestran el
QR + el alias para que el cliente transfiera.

Hay cuatro entregables, todos en `<proyecto>/data/`:
- `cartel_petscompany.png` — cartel base vertical.
- `cartel_petscompany_A4.pdf` — cartel para imprimir en A4.
- `sticker_petscompany.png` / `.pdf` — tarjeta chica para el mostrador.

El proyecto está, por defecto, en:
`D:\OneDrive\DCG y ROE - Diego\Diego Contabilidad\Antigravity\QR`

## Cómo regenerar (caso normal)

Con el QR oficial actual (no cambió el CVU), corré el orquestador:

```
python scripts/regenerar.py
```

Esto regenera los cuatro materiales. El script borra cada salida antes de
recrearla para esquivar el `OSError: [Errno 22]` que tira PIL al sobrescribir
archivos que OneDrive mantiene como placeholder (es el gotcha más común acá).

## Si cambió el CVU/CBU

El QR "oficial" (`assets/qr_oficial.png`) es un QR interoperable Coelsa/EMVCo que
codifica el CBU/CVU real. Si Diego te pasa un **CVU/CBU de 22 dígitos**, regeneralo
primero pasándolo al orquestador:

```
python scripts/regenerar.py --cbu <CVU22>
```

Opcionalmente podés pasar `--alias`, `--cuit`, `--titular` si cambiaron (sino usa
los defaults del proyecto: alias `petscompany`, CUIT `20330595516`, titular
"Diego Andres Echegaray").

Si el proyecto QR estuviera en otra ruta, agregá `--proyecto <ruta>`.

## Después de regenerar

Mostrale a Diego una vista previa de los resultados (al menos el sticker y el A4)
leyendo los archivos generados, para que confirme que quedaron bien. Si pide
ajustes de diseño (tamaños, colores, textos), esos viven en los scripts del
proyecto (`src/qr_petscompany.py`, `src/sticker_petscompany.py`,
`src/cartel_a4_pdf.py`) y en el kit `src/design_kit.py`.

## Notas

- **Idioma: español.** Confirmá antes de operaciones destructivas.
- **Git:** el repo está en `Antigravity/` (carpeta superior del proyecto QR).
  Si vas a commitear, stageá solo rutas explícitas de `QR/` (nunca `git add .`,
  hay ruido de OneDrive de otras carpetas).
- Requiere las dependencias del proyecto (`qrcode`, `Pillow`); ya están instaladas
  en el entorno de Diego.
