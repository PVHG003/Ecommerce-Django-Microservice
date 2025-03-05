ARG PYTHON_VERSION=3.13.2
FROM python:${PYTHON_VERSION} AS base

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    pip install --upgrade pip \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN #python manage.py makemigrations && python manage.py migrate

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]