FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . .

ENV UV_NO_DEV=1

RUN uv sync --locked

ENV DOCKER=1
ENV STORAGE_PATH=/app/storage/

CMD ["uv", "run", "app"]