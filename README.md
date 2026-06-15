# OSINT Engine

Motor OSINT open source para enriquecer radiografias con evidencia trazable,
fuentes publicas y reportes en JSON/Markdown.

Este repo no clona motores pesados adentro. En su lugar ofrece un nucleo propio,
liviano y auditable, con colectores gratuitos para dominios y adaptadores
opcionales para herramientas externas como SpiderFoot o theHarvester.

## Que hace hoy

- Recolecta DNS publicos: A, AAAA, MX, NS, TXT, SOA y CNAME.
- Consulta Certificate Transparency via `crt.sh`.
- Consulta Wayback Machine CDX para URLs historicas.
- Hace un probe HTTP/HTTPS basico: status, headers relevantes y titulo.
- Genera busquedas manuales listas para Google, Bing, GitHub, Wayback y crt.sh.
- Exporta una radiografia en JSON y Markdown con fuente, confianza y fecha.
- Incluye CLI, Dockerfile, tests y GitHub Actions.

## Limites legales y eticos

Usar solo fuentes publicas, abiertas y autorizadas. No evita captchas, logins,
paywalls, rate limits, robots.txt ni barreras tecnicas. No esta pensado para
doxxing, acoso, intrusiones o publicacion de datos sensibles. Para personas
privadas, minimizar datos y reportar solo informacion directamente relevante a
un objetivo legitimo.

## Instalacion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Alternativa simple:

```bash
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Uso rapido

```bash
python -m osint_engine domain example.com --out outputs/example
```

Esto crea:

- `outputs/example.json`
- `outputs/example.md`

Tests:

```bash
python -m unittest discover -s tests
```

Modo sin red, util para probar la CLI y generar dorks manuales:

```bash
python -m osint_engine domain example.com --offline --out outputs/example-offline
```

## Docker

```bash
docker build -t osint-engine .
docker run --rm -v "$PWD/outputs:/app/outputs" osint-engine domain example.com --out outputs/example
```

En PowerShell:

```powershell
docker build -t osint-engine .
docker run --rm -v "${PWD}\outputs:/app/outputs" osint-engine domain example.com --out outputs/example
```

## Integraciones externas opcionales

SpiderFoot es una herramienta OSINT open source con UI web, CLI, mas de 200
modulos y exportacion CSV/JSON/GEXF. theHarvester sirve para recolectar emails,
subdominios y nombres desde fuentes publicas. Este motor no las instala por
defecto para mantener el repo liviano, pero puede adjuntar resultados externos
cuando esten disponibles.

Ejemplo con theHarvester instalado en el sistema:

```bash
python -m osint_engine domain example.com --with-theharvester --out outputs/example
```

Si la herramienta no esta instalada, el reporte deja una nota de error no fatal.

## Estructura

```text
osint-engine/
  osint_engine/
    collectors/        # fuentes publicas gratuitas
    adapters/          # integraciones opcionales por CLI externa
    cli.py             # entrada de linea de comandos
    engine.py          # orquestacion
    models.py          # estructura de evidencia
    report.py          # JSON/Markdown
    safety.py          # validaciones de alcance
  tests/
  Dockerfile
  pyproject.toml
```

## Roadmap sugerido

- Ingesta de exportaciones SpiderFoot en JSON/CSV.
- Perfiles de fuentes para Argentina: boletines oficiales, contrataciones y
  registros societarios cuando sean publicos y autorizados.
- Salida Graphviz/Mermaid para mapas de vinculos.
- Job programado de GitHub Actions para monitoreo defensivo de dominios propios.
