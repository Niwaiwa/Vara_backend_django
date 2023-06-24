# Pull official base image 
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.3.2

RUN apt-get update \
    && apt-get install -y gcc python3-dev libffi-dev build-essential \
    libpq-dev

# RUN cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
#     && echo "Asia/Taipei" > /etc/timezone

COPY poetry.lock pyproject.toml /app/

RUN pip install "poetry==$POETRY_VERSION"

#RUN poetry config virtualenvs.create false
# Install dependencies
RUN poetry install --no-interaction --no-ansi

COPY . /app/
# RUN python manage.py migrate 

CMD ["gunicorn" , "--config" , "gunicorn_config.py" , "vara_backend.wsgi:application" ]