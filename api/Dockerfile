FROM python:3.9

EXPOSE 8000

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml /

RUN poetry install --no-dev
COPY ./src /app

WORKDIR /app

CMD ["poetry", "run", "uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "main:app"]
