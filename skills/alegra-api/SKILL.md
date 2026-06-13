---
name: alegra-api
description: >
  Consulta y analiza ventas, facturas, productos y medios de pago desde la API de Alegra
  para Pets Company (veterinaria/petshop, San Juan, Argentina). Úsala siempre que el usuario
  pregunte por ventas del día, semana o mes; cómo fue la mañana o la tarde; qué se vendió;
  cuánto se facturó; análisis por medio de pago; detalle de una factura; búsqueda por producto
  o referencia; o cualquier consulta sobre datos comerciales. También aplica cuando el usuario
  diga "cómo fueron las ventas", "qué vendimos", "cuánto hicimos hoy/ayer/esta semana",
  "detalle de la factura X", "buscá el producto Y", o frases similares relacionadas con
  movimientos comerciales del negocio.
---

# Ejecución de Skill: alegra-api

Esta skill se comunica con la API de Alegra de Pets Company. Para realizar las tareas analíticas de manera óptima, eficiente y determinista, sigue estrictamente las instrucciones siguientes:

## 1. Usar el Script Analítico de Consultas (Obligatorio)

Toda la lógica de análisis de datos, agregación, comparación de turnos, agrupación por medio de pago y filtros de producto debe ejecutarse importando las funciones predefinidas del script [`scripts/consultas.py`](scripts/consultas.py). **NUNCA** implementes esta lógica en prosa o mediante código ad-hoc:

```python
from alegra_client import AlegraClient
import consultas

cli = AlegraClient()

# 1. Ventas generales del día
res_ventas = consultas.analizar_ventas(cli, "2026-05-23")

# 2. Ventas por turno (Mañana vs Noche)
res_turnos = consultas.analizar_turnos(cli, "2026-05-23")

# 3. Detalle de factura específica
factura = consultas.buscar_detalle_factura(res_ventas["facturas"], "00001252")

# 4. Ventas por producto o referencia
res_prod = consultas.analizar_ventas_producto(cli, "Alimento Perro", "2026-05-20", "2026-05-23")

# 5. Ventas por medio de pago
res_pagos = consultas.analizar_por_medio_pago(cli, "2026-05-23")

# 6. Distribución por horarios
res_horas = consultas.analizar_por_horario(cli, "2026-05-23")
```

## 2. Documentación y Recursos de Referencia (Carga Progresiva)

Si necesitas detalles específicos de la API o guías analíticas, lee los siguientes archivos bajo demanda:

- **Contexto del negocio:** Consulta [`references/contexto-negocio.md`](references/contexto-negocio.md) si necesitas datos fiscales de Pets Company o información sobre horarios.
- **Autenticación:** Consulta [`references/api-auth.md`](references/api-auth.md) si requieres detalles técnicos de credenciales o ejemplos directos con `curl`.
- **Limitaciones de la API:** Consulta [`references/api-limitaciones.md`](references/api-limitaciones.md) si tienes problemas de paginación u otros comportamientos erráticos de la API.
- **Paginación y filtrado manual:** Consulta [`references/api-paginacion.md`](references/api-paginacion.md) si necesitas ver cómo se estructura la paginación y deduplicación de forma nativa en Python.
- **Guía de consultas frecuentes:** Consulta [`references/consultas-frecuentes.md`](references/consultas-frecuentes.md) para saber cómo estructurar el razonamiento y qué funciones específicas de `consultas.py` invocar para cada pregunta de Diego.
- **Formato del reporte final:** Consulta [`references/formato-respuesta.md`](references/formato-respuesta.md) para asegurar que el resumen de ventas, las tablas markdown y el mapeo de medios de pago sigan la estructura preferida por Diego.

## 3. Caché Temporal
- Utiliza la ruta temporal `/tmp/alegra_*.json` para almacenar las páginas de facturas descargadas de una misma sesión para no agotar la cuota de la API.
