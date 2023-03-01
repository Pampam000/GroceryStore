FROM python:3.10
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.3.2

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

WORKDIR /project
COPY poetry.lock pyproject.toml  /project/

RUN poetry lock --no-update && \
    poetry install

COPY . /project

#RUN poetry run python app/manage.py migrate
#CMD ["poetry", "run", "python", "app/manage.py", "migrate"]









