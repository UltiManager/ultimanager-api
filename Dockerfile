FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Copy entrypoint to accessible location
COPY docker-entrypoint.sh /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]

# Install Dependencies
RUN apk add --no-cache build-base libjpeg-turbo-dev postgresql-client postgresql-dev zlib-dev
RUN pip install --upgrade pip pipenv

# Install Python Dependencies
WORKDIR /opt/ultimanager-api
COPY Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile --system

# Copy application source code
COPY . /opt/ultimanager-api

# Entrypoints into application
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["server", "--bind", "0.0.0.0:8000"]
