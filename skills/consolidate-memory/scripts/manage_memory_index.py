# -*- coding: utf-8 -*-
"""Administrador del Índice de Memoria (MEMORY.md).

Valida que todos los archivos enlazados en MEMORY.md existan en el disco,
elimina enlaces rotos, detecta archivos de memoria que no están enlazados,
remueve duplicados y normaliza el formato de las líneas.
"""

import os
import sys
import re
from pathlib import Path

def tidy_memory_index(memory_dir: Path):
    index_path = memory_dir / "MEMORY.md"
    if not index_path.exists():
        print(f"Error: No se encontró MEMORY.md en {memory_dir}")
        return False
        
    print(f"Leyendo índice: {index_path}")
    content = index_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    header_lines = []
    index_lines = []
    
    # Separar el header del contenido del índice
    in_index = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- [") and "]" in stripped and "(" in stripped:
            in_index = True
        
        if in_index:
            if stripped.startswith("- ["):
                index_lines.append(stripped)
        else:
            header_lines.append(line)
            
    print(f"Líneas de índice detectadas: {len(index_lines)}")
    
    # Obtener todos los archivos .md en el directorio
    all_files = {f.name for f in memory_dir.glob("*.md") if f.name != "MEMORY.md"}
    
    cleaned_lines = []
    linked_files = set()
    vistos = set()
    
    # Validar y limpiar enlaces existentes
    for line in index_lines:
        match = re.match(r"^-\s*\[([^\]]+)\]\(([^)]+)\)\s*(?:—\s*(.*))?$", line)
        if not match:
            # Línea mal formateada pero la conservamos de momento
            cleaned_lines.append(line)
            continue
            
        title, filename, hook = match.groups()
        filename = filename.strip()
        
        # Ignorar si es un link duplicado
        if filename in vistos:
            continue
        vistos.add(filename)
        
        file_path = memory_dir / filename
        if file_path.exists():
            linked_files.add(filename)
            formatted_hook = f" — {hook.strip()}" if hook else ""
            cleaned_lines.append(f"- [{title.strip()}]({filename}){formatted_hook}")
        else:
            print(f"  ✗ Eliminando enlace roto: {filename} ({title})")
            
    # Detectar archivos huérfanos (no enlazados en MEMORY.md)
    unlinked_files = all_files - linked_files
    if unlinked_files:
        print("\nAlertas de archivos no enlazados en MEMORY.md:")
        for f in sorted(unlinked_files):
            print(f"  • {f} (huérfano)")
            # Agregamos automáticamente al índice
            title_suggested = f.replace(".md", "").replace("-", " ").title()
            cleaned_lines.append(f"- [{title_suggested}]({f}) — Nuevo archivo de memoria detectado.")
            
    # Escribir el nuevo archivo MEMORY.md
    new_content = "\n".join(header_lines).strip() + "\n\n" + "\n".join(cleaned_lines) + "\n"
    index_path.write_text(new_content, encoding="utf-8")
    
    print("\n=== Limpieza de índice completada ===")
    print(f"Total de entradas activas: {len(cleaned_lines)}")
    return True

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    if len(sys.argv) > 1:
        memory_dir = Path(sys.argv[1])
    else:
        # Intentar buscar en ubicaciones estándar
        posibles = [
            Path.home() / ".gemini" / "antigravity-ide" / "brain" / "memory",
            Path.cwd() / "brain" / "memory",
            Path.cwd() / "memory",
            Path.cwd().parent / "brain" / "memory"
        ]
        memory_dir = None
        for p in posibles:
            if p.exists() and (p / "MEMORY.md").exists():
                memory_dir = p
                break
                
        if not memory_dir:
            print("Error: No se especificó el directorio de memoria y no se detectó automáticamente.")
            print("Uso: python manage_memory_index.py <ruta_directorio_memoria>")
            sys.exit(1)
            
    tidy_memory_index(memory_dir)

if __name__ == "__main__":
    main()
