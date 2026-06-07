# Calendario de Informes Diarios (Getnet)

Este archivo contiene la planificación de establecimientos y propietarios que deben ejecutarse automáticamente cuando Diego solicite informes según el día de la semana.

---

## 1. Informe de Domingo (Flujo Automático)
Cuando Diego diga **"informe de domingo"**, ejecuta automáticamente el proceso descarga ➔ informe para los siguientes establecimientos en este orden:

| Orden | Establecimiento | Propietario para el Informe |
|---|---|---|
| 1° | DCG 1 | Ayrton Gil |
| 2° | DCG 5 | Lucas Balmaceda |
| 3° | DCG 7 | Jose Castro |
| 4° | DCG 9 | Pets Company |

---

## 2. Informe de Miércoles (Flujo Automático)
Cuando Diego diga **"informe de miércoles"**, ejecuta para:

| Orden | Establecimiento | Propietario para el Informe |
|---|---|---|
| 1° | DCG 4 | Martin Costa |

---

## 3. Informe de Jueves (Flujo Automático)
Cuando Diego diga **"informe de jueves"**, ejecuta para:

| Orden | Establecimiento | Propietario para el Informe |
|---|---|---|
| 1° | DCG 2 | Jacqueline Muñoz |
| 2° | DCG 8 | Sebastián Mas |

---

## 4. Consulta Canónica de Establecimientos
Si Diego solicita informes para otros establecimientos que no figuren en las listas anteriores, consulta la lista canónica y sus respectivos propietarios directamente en el archivo [`references/establecimientos.json`](establecimientos.json).
