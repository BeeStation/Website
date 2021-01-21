from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import redirect

bp_redirects = Blueprint('redirects', __name__)

@bp_redirects.route("/rules/rp") # Temporary as I get crossed to update the rules urls everywhere
def page_rules_tempredirect():
	return redirect("/rules?server=bs_sage")


@bp_redirects.route("/join/<string:id>")
def page_join(id):
	try:
		server = util.get_server(id)
		return redirect("byond://{}:{}".format(server["host"],server["port"]))
	except Exception as E:
		pass


@bp_redirects.route("/forum")
def page_forum():
	return redirect("https://bing.com")