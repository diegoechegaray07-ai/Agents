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

Pets Company cobra **por transferencia de Mercado Pago** (alias `petscompany`), no con el QR de cobro de MP (que tiene comisión). Estos materiales muestran el QR + el alias para que el cliente transfiera.

Hay cuatro entregables, todos guardados en `<proyecto>/data/`:
- `cartel_petscompany.png` — cartel base vertical.
- `cartel_petscompany_A4.pdf` — cartel para imprimir en A4.
- `sticker_petscompany.png` / `.pdf` — tarjeta chica para el mostrador.

El proyecto está en la ruta local:
`D:\OneDrive\DCG y ROE - Diego\Diego\Antigravity\QR`
(en Mac: `.../OneDrive-Personal/DCG y ROE - Diego/Diego/Antigravity/QR`)

## 1. Cómo regenerar (Caso Normal)

Con el QR oficial actual (sin cambios de CVU), ejecuta el orquestador:

```bash
python scripts/regenerar.py
```

*Nota: El script borra cada archivo de salida antes de recrearlo para evitar el `OSError: [Errno 22]` que arroja PIL al intentar sobrescribir archivos que OneDrive mantiene como placeholder.*

## 2. Si cambió el CVU/CBU (Actualización de QR)

El QR oficial (`assets/qr_oficial.png`) codifica el CBU/CVU real (Coelsa/EMVCo). Si Diego te indica un **CVU/CBU de 22 dígitos**, actualízalo primero pasándolo al orquestador:

```bash
python scripts/regenerar.py --cbu <CVU22>
```

Opcionalmente, puedes especificar `--alias`, `--cuit` o `--titular` si han cambiado (de lo contrario utilizará los valores predeterminados del proyecto: alias `petscompany`, CUIT `20330595516`, titular "Diego Andres Echegaray"). Si el proyecto QR estuviese en otra ruta, agrega `--proyecto <ruta>`.

## 3. Guías de Verificación y Notas de Desarrollo

Consulta el siguiente archivo de referencia tras finalizar la generación o si necesitas editar el diseño:
- **Instrucciones adicionales y notas de desarrollo:** Consulta [`references/instrucciones-adicionales.md`](references/instrucciones-adicionales.md) para ver la guía de validación visual, listado de scripts del código fuente y notas sobre Git.
