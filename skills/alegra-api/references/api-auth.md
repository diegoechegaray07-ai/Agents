# Credenciales y Autenticación de API de Alegra

Este archivo detalla cómo interactuar técnicamente con la API de Alegra si no estás utilizando el cliente compartido de Python.

## Detalles Técnicos de la API
- **Base URL:** `https://app.alegra.com/api/v1/`
- **Método de Autenticación:** HTTP Basic Auth.
  - Las credenciales no se deben incluir en el código ni en las instrucciones generales.
  - Se leen del entorno (`.env`) mediante las variables `ALEGRA_USER` (o `ALEGRA_EMAIL`) y `ALEGRA_TOKEN`.

## Ejemplo de uso con curl
Si necesitas realizar una petición directa usando `curl` desde la consola Bash/PowerShell:

```bash
# Carga las variables de entorno de la skill y realiza la petición
set -a; source .env; set +a
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "https://app.alegra.com/api/v1/invoices?limit=30&start=0"
```
