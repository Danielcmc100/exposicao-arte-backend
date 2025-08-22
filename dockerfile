FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

COPY . .

RUN uv sync

CMD ["uv", "run", "fastapi", "run", "src/app.py", "--port", "8080", "--host", "0.0.0.0"]

