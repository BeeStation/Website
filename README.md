# BeeStation Website

## Hosting

In order to properly host, you must fill out `src/app/config/private.yml`

### Docker (Recommended)

#### Development

Run `docker-compose -f docker-compose.dev.yml up --build`

This will build the docker image and start hosting on port `8080` by default. Using this compose file will also enable uwsgi's debugging and auto-reloading of changed application files.

#### Production

Create a new directory on your target system and run `curl -L deploy.beestation13.buzz/website | bash` within that directory. Doing so will download the necessary files and prepare the docker environment.

See `setup.sh` for the actual installation steps.

### Direct

#### Development

For direct development hosting, simply run `src/wsgi.py`

#### Production

For production hosting, use `uwsgi` to serve `server-conf/beesite_uwsgi.ini` to a socket file `beesite_uwsgi.sock`. 

You will need to either use nginx (recommended) or apache to read and serve from the uwsgi socket.
