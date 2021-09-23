import yaml

WEBSITE = yaml.load(open("app/config/website.yml"), Loader=yaml.SafeLoader)
SERVERS = yaml.load(open("app/config/servers.yml"), Loader=yaml.SafeLoader)
