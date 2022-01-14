# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends default-libmysqlclient-dev gcc git && \
    pip install pipenv

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile

RUN apt-get autoremove gcc git --purge -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

COPY server-conf/beesite_uwsgi.ini /etc/uwsgi/uwsgi.ini

WORKDIR /beesite
COPY /src /beesite

RUN gzip --keep --best --force --recursive /beesite/app/static/ && \
    chown -R www-data:www-data /beesite

USER www-data:www-data

EXPOSE 8080

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
