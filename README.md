# Agents

Repositorio de agentes de IA.

## Estructura

```
src/
  agents/    # Definición de los agentes
  tools/     # Herramientas que usan los agentes
  utils/     # Utilidades compartidas
  config/    # Configuración
tests/       # Tests unitarios e integración
docs/        # Documentación
data/        # Datos de muestra y salidas
scripts/     # Scripts de setup y despliegue
```

## Requisitos

- Python 3.11+

## Instalación

```bash
git clone https://github.com/<usuario>/Agents.git
cd Agents
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Configuración

Copiá `.env.example` a `.env` y completá tus claves:

```bash
cp .env.example .env
```

## Uso

```bash
python -m src.agents
```

## Tests

```bash
pytest tests/
```

## Licencia

MIT — ver [LICENSE](LICENSE).
