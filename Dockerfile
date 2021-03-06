FROM python:3.7-alpine

ARG VERSION=unknown

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy entrypoint to accessible location
COPY docker-entrypoint.sh /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]

# Install Dependencies
RUN apk add --no-cache build-base libjpeg-turbo-dev postgresql-client postgresql-dev zlib-dev
RUN pip install --upgrade pip pipenv

# Copy application
WORKDIR /opt/ultimanager-web
COPY . /opt/ultimanager-web

# Persist Commit Hash
RUN echo $VERSION > /opt/ultimanager-web/VERSION

# Install Third Party Packages
RUN pipenv install --ignore-pipfile --system

# Entrypoints into application
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["server", "--bind", "0.0.0.0:8000"]
