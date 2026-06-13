# -*- coding: utf-8 -*-
"""Módulo de consultas analíticas sobre la API de Alegra.

Contiene funciones para analizar ventas, comparar turnos, filtrar por producto,
agrupar por medio de pago y analizar horarios de venta.
"""

import sys
from pathlib import Path

# Agregar la ruta del cliente compartido al path
SHARED_DIR = str(Path(__file__).resolve().parent.parent.parent / "_shared")
if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)

from alegra_client import AlegraClient, map_payment_method, turno


def analizar_ventas(client: AlegraClient, fecha_inicio: str, fecha_fin: str = None) -> dict:
    """Calcula métricas generales de ventas en un período."""
    if not fecha_fin:
        fecha_fin = fecha_inicio
    facturas = client.invoices_between(fecha_inicio, fecha_fin)
    
    totales = [float(f.get("total", 0)) for f in facturas]
    num_transacciones = len(totales)
    total_facturado = sum(totales)
    ticket_promedio = total_facturado / num_transacciones if num_transacciones > 0 else 0
    max_venta = max(totales) if totales else 0
    min_venta = min(totales) if totales else 0
    
    return {
        "facturas": facturas,
        "total_facturado": total_facturado,
        "cantidad_transacciones": num_transacciones,
        "ticket_promedio": ticket_promedio,
        "max_venta": max_venta,
        "min_venta": min_venta
    }


def analizar_turnos(client: AlegraClient, fecha: str) -> dict:
    """Clasifica y compara las ventas de la mañana vs la tarde/noche."""
    facturas = client.invoices_on(fecha)
    
    turnos = {"Mañana": {"total": 0.0, "cantidad": 0}, "Noche": {"total": 0.0, "cantidad": 0}}
    for f in facturas:
        t = turno(f.get("datetime"))
        monto = float(f.get("total", 0))
        if t in turnos:
            turnos[t]["total"] += monto
            turnos[t]["cantidad"] += 1
            
    return turnos


def buscar_detalle_factura(facturas: list, numero_formateado: str) -> dict:
    """Busca y devuelve el detalle completo de una factura por su número (ej. '00001252')."""
    for f in facturas:
        num = (f.get("numberTemplate") or {}).get("formattedNumber")
        if num == numero_formateado:
            return {
                "id": f.get("id"),
                "numero": num,
                "fecha": f.get("date"),
                "fecha_hora": f.get("datetime"),
                "cliente": (f.get("client") or {}).get("name", "Desconocido"),
                "items": [
                    {
                        "nombre": item.get("name"),
                        "referencia": item.get("reference"),
                        "cantidad": float(item.get("quantity", 0)),
                        "precio": float(item.get("price", 0)),
                        "total": float(item.get("total", 0))
                    } for item in f.get("items", [])
                ],
                "subtotal": float(f.get("subtotal", 0)),
                "impuestos": float(f.get("tax", 0)),
                "total": float(f.get("total", 0)),
                "pagos": [
                    {
                        "medio": map_payment_method(p.get("paymentMethod")),
                        "monto": float(p.get("value", 0))
                    } for p in f.get("payments", [])
                ]
            }
    return None


def analizar_ventas_producto(client: AlegraClient, query: str, fecha_inicio: str, fecha_fin: str = None) -> dict:
    """Analiza las ventas de un producto específico (por nombre o referencia)."""
    if not fecha_fin:
        fecha_fin = fecha_inicio
    facturas = client.invoices_between(fecha_inicio, fecha_fin)
    
    ventas = []
    total_recaudado = 0.0
    cantidad_vendida = 0.0
    
    for f in facturas:
        for item in f.get("items", []):
            name = item.get("name", "")
            ref = item.get("reference", "")
            if query.lower() in name.lower() or query.lower() in ref.lower():
                cant = float(item.get("quantity", 0))
                total_item = float(item.get("total", 0))
                total_recaudado += total_item
                cantidad_vendida += cant
                ventas.append({
                    "factura": (f.get("numberTemplate") or {}).get("formattedNumber", f.get("id")),
                    "fecha": f.get("date"),
                    "nombre": name,
                    "referencia": ref,
                    "cantidad": cant,
                    "total": total_item
                })
                
    return {
        "query": query,
        "coincidencias": ventas,
        "total_recaudado": total_recaudado,
        "cantidad_vendida": cantidad_vendida
    }


def analizar_por_medio_pago(client: AlegraClient, fecha_inicio: str, fecha_fin: str = None) -> dict:
    """Agrupa la facturación según los medios de pago utilizados."""
    if not fecha_fin:
        fecha_fin = fecha_inicio
    facturas = client.invoices_between(fecha_inicio, fecha_fin)
    
    medios = {}
    total_general = 0.0
    
    for f in facturas:
        for p in f.get("payments", []):
            metodo_raw = p.get("paymentMethod", "other")
            metodo = map_payment_method(metodo_raw)
            valor = float(p.get("value", 0))
            
            if metodo not in medios:
                medios[metodo] = {"total": 0.0, "operaciones": 0}
            medios[metodo]["total"] += valor
            medios[metodo]["operaciones"] += 1
            total_general += valor
            
    # Calcular porcentajes
    for m in medios:
        medios[m]["porcentaje"] = (medios[m]["total"] / total_general * 100) if total_general > 0 else 0
        
    return {
        "medios": medios,
        "total_general": total_general
    }


def analizar_por_horario(client: AlegraClient, fecha_inicio: str, fecha_fin: str = None) -> dict:
    """Distribuye las ventas por hora entera para determinar picos de concurrencia."""
    if not fecha_fin:
        fecha_fin = fecha_inicio
    facturas = client.invoices_between(fecha_inicio, fecha_fin)
    
    horas = {}
    for f in facturas:
        dt = f.get("datetime")
        if not dt:
            continue
        try:
            hora = int(dt[11:13])
        except (ValueError, TypeError, IndexError):
            continue
            
        monto = float(f.get("total", 0))
        if hora not in horas:
            horas[hora] = {"total": 0.0, "transacciones": 0}
        horas[hora]["total"] += monto
        horas[hora]["transacciones"] += 1
        
    # Ordenar por hora
    horas_ordenadas = dict(sorted(horas.items()))
    return horas_ordenadas
