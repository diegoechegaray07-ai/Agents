# -*- coding: utf-8 -*-
"""Script multiplataforma para respaldar las skills activas de Claude en OneDrive.

Busca la carpeta de skills activa de Claude (en macOS o Windows) e interactúa
con el directorio de destino en OneDrive para copiar de forma incremental las
habilidades configuradas.
"""

import os
import sys
import shutil
import glob
from pathlib import Path

def get_default_origin() -> Path:
    """Intenta autodetectar el directorio de origen de las skills de Claude."""
    home = Path.home()
    
    # 1. Definir rutas base por sistema operativo
    if sys.platform == "win32":
        base_path = home / "AppData" / "Roaming" / "Claude" / "local-agent-mode-sessions" / "skills-plugin"
    elif sys.platform == "darwin":
        base_path = home / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions" / "skills-plugin"
    else:
        # Linux u otros
        base_path = home / ".config" / "Claude" / "local-agent-mode-sessions" / "skills-plugin"

    if not base_path.exists():
        return None

    # 2. Las skills se ubican en: .../skills-plugin/<uuid>/<uuid>/skills/
    # Buscamos usando un patrón glob
    pattern = str(base_path / "*" / "*" / "skills")
    matches = glob.glob(pattern)
    
    if matches:
        # Retorna el primer match encontrado
        return Path(matches[0])
    return None

def get_default_destination() -> Path:
    """Intenta autodetectar la ruta de destino en OneDrive del usuario."""
    home = Path.home()
    
    # Rutas candidatas de OneDrive. La carpeta "Diego Contabilidad" se renombró a
    # "Diego" en jun-2026; OneDrive propaga el rename a todas las máquinas.
    candidates = [
        home / "Library" / "CloudStorage" / "OneDrive-Personal" / "DCG y ROE - Diego" / "Diego" / "Antigravity" / "Skills",
        home / "OneDrive" / "DCG y ROE - Diego" / "Diego" / "Antigravity" / "Skills",
        Path("D:/OneDrive/DCG y ROE - Diego/Diego/Antigravity/Skills"),
        Path("D:/OneDrive - Diego/Diego/Antigravity/Skills"),
    ]
    
    for c in candidates:
        if c.exists() or c.parent.exists():
            return c
            
    return None

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    print("=== Iniciando Respaldo de Habilidades ===")
    
    # Cargar rutas de variables de entorno o autodetectar
    origin_env = os.environ.get("CLAUDE_SKILLS_DIR")
    dest_env = os.environ.get("ONEDRIVE_BACKUP_DIR")
    
    origin = Path(origin_env) if origin_env else get_default_origin()
    destination = Path(dest_env) if dest_env else get_default_destination()
    
    # Si sigue sin encontrarse, pedir verificación
    if not origin or not origin.exists():
        print(f"Error: No se pudo localizar la carpeta de origen de Claude.")
        print(f"Buscado en base: {Path.home() / 'AppData/Roaming/Claude/.../skills'}")
        print("Define la variable CLAUDE_SKILLS_DIR en tu entorno o archivo .env")
        sys.exit(1)
        
    if not destination:
        print("Error: No se pudo localizar la carpeta de destino de OneDrive.")
        print("Define la variable ONEDRIVE_BACKUP_DIR en tu entorno o archivo .env")
        sys.exit(1)

    print(f"Origen (Claude):  {origin}")
    print(f"Destino (OneDrive): {destination}")
    print()

    # Asegurar que existe el destino
    destination.mkdir(parents=True, exist_ok=True)

    # Copiar carpetas de habilidades
    copied_count = 0
    for item in origin.iterdir():
        if item.is_dir() and not item.name.startswith((".", "_")):
            dest_item = destination / item.name
            try:
                # Si ya existe, lo eliminamos para sobreescribir limpiamente
                if dest_item.exists():
                    shutil.rmtree(dest_item)
                shutil.copytree(item, dest_item)
                print(f"  ✓ {item.name}")
                copied_count += 1
            except Exception as e:
                print(f"  ✗ {item.name} (Error: {e})")

    print()
    print(f"Respaldo completado. {copied_count} habilidades copiadas con éxito.")
    print(f"Ubicación de copia: {destination}")

if __name__ == "__main__":
    main()
