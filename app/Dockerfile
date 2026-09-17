FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

WORKDIR /app

ENV UV_NO_DEV=1

RUN uv sync --locked

CMD ["uv", "run", "fastapi", "run", "src/app/main.py"]