from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import redirect
from flask import request

bp_redirects = Blueprint('redirects', __name__)

@bp_redirects.route("/join/<string:id>")
def page_join(id):
	try:
		server = util.get_server(id)
		return redirect("byond://{}:{}".format(server["host"],server["port"]))
	except Exception as E:
		pass


@bp_redirects.route("/rules")
def page_rules():
	server_id = request.args.get('server', type=str, default=util.get_server_default()["id"])
	server = util.get_server(server_id)

	if not server:
		return abort(404)

	return redirect(server["rules_url"])


@bp_redirects.route("/forum")
def page_forum():
	return redirect("https://forums.beestation13.com")

@bp_redirects.route("/uptime")
def page_uptime():
	return redirect("https://status.beestation13.com")