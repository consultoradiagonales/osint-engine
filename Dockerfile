FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY osint_engine ./osint_engine

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "osint_engine"]
