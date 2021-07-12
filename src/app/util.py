from app import cfg

import re

def to_ckey(byondkey):
	return re.sub(r'[^a-zA-Z0-9]', '', byondkey).lower()

def get_server(id):
	for server in cfg.SERVERS:
		if server["id"] == id:
			return server

def get_server_from_alias(alias):
	for server in cfg.SERVERS:
		if alias in server["aliases"] or alias == server["id"]:
			return server

def get_server_default():
	return cfg.SERVERS[0]