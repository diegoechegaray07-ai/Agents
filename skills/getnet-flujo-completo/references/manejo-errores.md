# Manejo de Errores Frecuentes (Getnet Portal)

Este archivo contiene soluciones a los problemas de red, navegador o sesión que suelen ocurrir durante la automatización del portal de Getnet.

| Problema / Síntoma | Causa Probable | Acción Correctiva / Solución |
|---|---|---|
| **Expiración de Sesión** (Redirección a login) | El token del portal de Getnet expiró por inactividad. | Avisa inmediatamente a Diego en el chat, solicita que inicie sesión manualmente y espera su confirmación ("listo") antes de navegar de nuevo a `/s/transactions`. |
| **Timeout de Captura de Pantalla** | La página web demoró en renderizar sus elementos o la red está lenta. | Espera 8-10 segundos adicionales y vuelve a intentar tomar la captura de pantalla o ejecutar la acción. |
| **Navegador Desconectado** | La extensión MCP perdió la conexión con el proceso del navegador Chrome. | Llama en orden: `list_connected_browsers` ➔ `select_browser` para reconectar y reintenta el flujo. |
| **Establecimiento Incorrecto** al Descargar | El portal cargó por defecto el último local consultado en la sesión anterior. | Asegúrate de verificar el selector superior derecho antes de descargar el archivo. Si no coincide, cámbialo en "Mis establecimientos". |
| **Permiso Denegado** en `www.globalgetnet.com` | La extensión MCP de Chrome no posee permisos para el subdominio `www.`. | **NUNCA** utilices o navegues a la URL con `www`. Navega directamente a `portal.globalgetnet.com/s/transactions`. |
