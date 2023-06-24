import yaml

WEBSITE = yaml.load(open("beesite/config/website.yml"), Loader=yaml.SafeLoader)
SERVERS = yaml.load(open("beesite/config/servers.yml"), Loader=yaml.SafeLoader)
