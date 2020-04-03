import yaml

WEBSITE = yaml.load(open("app/config/website.yml"))
SERVERS = yaml.load(open("app/config/servers.yml"))
MAPS = yaml.load(open("app/config/maps.yml"))
PRIVATE = yaml.load(open("app/config/private.yml"))