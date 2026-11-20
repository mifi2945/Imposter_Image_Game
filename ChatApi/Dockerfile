FROM python:3.13-slim
WORKDIR /api

RUN python -m pip install uv

COPY . .
RUN uv sync --no-dev

CMD ["uv", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]