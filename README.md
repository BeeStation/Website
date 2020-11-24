# BeeStation Website

## Hosting

In order to properly host, you must fill out `app/config/private.yml`

**Development**

For development hosting, simply run `wsgi.py`

**Production**

For production hosting, use `uwsgi` to serve `beesite_uwsgi.ini` to a socket file `beesite_uwsgi.sock`

Use nginx with the configuration `beesite_nginx.conf` to read the socket file and serve it publicly