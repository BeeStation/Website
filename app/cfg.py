import yaml

WEBSITE	= yaml.load(open("app/config/website.yml"),	Loader=yaml.SafeLoader)
SERVERS	= yaml.load(open("app/config/servers.yml"),	Loader=yaml.SafeLoader)
MAPS	= yaml.load(open("app/config/maps.yml"),	Loader=yaml.SafeLoader)
PRIVATE	= yaml.load(open("app/config/private.yml"),	Loader=yaml.SafeLoader)