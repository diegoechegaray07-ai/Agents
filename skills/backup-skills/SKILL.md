---
name: backup-skills
description: >
  Realiza una copia de seguridad o respaldo de todas las habilidades de Claude
  hacia la carpeta configurada en OneDrive. Úsala siempre que el usuario cree una
  nueva habilidad, edite alguna existente, o pida "hacer backup de las skills",
  "sincronizar habilidades", "guardar mis skills en OneDrive" o frases afines.
  También debe sugerirse automáticamente al finalizar cualquier flujo de creación
  o edición de habilidades.
---

# Ejecución de Skill: backup-skills

Esta habilidad respalda las habilidades activas de Claude en la carpeta de OneDrive.

## 1. Ejecutar el Respaldo (Python)

Ejecuta el script multiplataforma en Python para realizar la copia incremental y sobreescribir las versiones anteriores en OneDrive de manera segura:

```bash
python scripts/backup.py
```

*Nota: El script autodetectará la carpeta activa de Claude y la carpeta de OneDrive tanto en Windows como en macOS. Si necesitas forzar rutas personalizadas, define las variables de entorno `CLAUDE_SKILLS_DIR` y `ONEDRIVE_BACKUP_DIR` en el archivo `.env` o en el entorno.*

## 2. Formato de Respuesta de Confirmación
Tras completar la copia, muestra a Diego:
1. La lista de habilidades respaldadas individualmente con un icono de check `✓`.
2. La cantidad total de habilidades copiadas.
3. La ruta de destino en OneDrive confirmada.

## 3. Disparo Automático
Cuando finalices el proceso de creación o edición de cualquier habilidad en el chat, sugiere a Diego realizar el backup inmediatamente:
> "¿Querés que guarde el backup en OneDrive ahora?"
