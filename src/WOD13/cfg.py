import yaml

WEBSITE = yaml.load(open("WOD13/config/website.yml"), Loader=yaml.SafeLoader)
SERVERS = yaml.load(open("WOD13/config/servers.yml"), Loader=yaml.SafeLoader)
