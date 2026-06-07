---
name: backup-skills
description: >
  Hace una copia de respaldo de todas las skills instaladas en Claude hacia la carpeta
  de OneDrive. Úsala siempre que el usuario cree una nueva skill, modifique una existente,
  o pida "hacer backup de skills", "guardar skills", "sincronizar skills", "respaldar skills",
  "copiar skills a OneDrive" o frases similares. También debe ejecutarse automáticamente
  al final de cualquier proceso de creación o edición de una skill.
---

## Qué hace esta skill

Copia todas las skills instaladas en Claude hacia la carpeta de respaldo en OneDrive, sobreescribiendo versiones anteriores para mantenerla actualizada.

## Rutas

- **Origen (skills activas):**
  `/Users/diegoaechegaray/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/dbe69af9-c783-459f-bd6b-185995f31aaa/9bf4f2be-d17f-43ea-af0f-d29e88269168/skills/`

- **Destino (respaldo OneDrive):**
  `/Users/diegoaechegaray/Library/CloudStorage/OneDrive-Personal/DCG y ROE - Diego/Diego Contabilidad/Antigravity/Skills/`

## Cómo ejecutar el backup

Correr este comando:

```bash
ORIGEN="/Users/diegoaechegaray/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/dbe69af9-c783-459f-bd6b-185995f31aaa/9bf4f2be-d17f-43ea-af0f-d29e88269168/skills"
DESTINO="/Users/diegoaechegaray/Library/CloudStorage/OneDrive-Personal/DCG y ROE - Diego/Diego Contabilidad/Antigravity/Skills"

for skill in "$ORIGEN"/*/; do
  nombre=$(basename "$skill")
  rm -rf "$DESTINO/$nombre"
  cp -r "$skill" "$DESTINO/$nombre"
  echo "✓ $nombre"
done

echo ""
echo "Backup completo. Skills en OneDrive:"
ls "$DESTINO"
```

## Formato de respuesta

Después de ejecutar, mostrar:

1. Lista de skills copiadas con ✓
2. Total de skills respaldadas
3. Ruta de destino confirmada

## Cuándo ejecutar automáticamente

Siempre que en la conversación se haya creado o modificado una skill, al finalizar el proceso ofrecer hacer el backup:
> "¿Querés que guarde el backup en OneDrive?"

Si el usuario confirma o dice "sí", ejecutar el backup sin más preguntas.
