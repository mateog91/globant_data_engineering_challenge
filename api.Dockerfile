FROM python:3.9

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /api

COPY ./pyproject.toml /api/pyproject.toml

COPY ./poetry.lock /api/poetry.lock

RUN poetry install

COPY ./api /api

RUN alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]