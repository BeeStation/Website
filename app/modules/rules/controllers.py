from app import cfg
from app import db
from app import util

from flask import abort
from flask import Blueprint
from flask import render_template
from flask import request

import json

bp_rules = Blueprint('rules', __name__)

@bp_rules.route("/rules")
def page_rules():
	alias = request.args.get('server', type=str, default="bee")
	server = util.get_server_from_alias(alias)

	if not server:
		return abort(404)

	return render_template("rules.html", rules=json.load(open("config/rules/{}.json".format(server["id"]))))

