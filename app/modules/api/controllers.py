from app import cfg
from app import db
from app import util

from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

bp_api = Blueprint('api', __name__, url_prefix='/api')

@bp_api.route("/stats")
def page_api_stats():
	try:
		d = {}

		for server in cfg.SERVERS:
			if server["open"]:
				try:
					d[server["id"]] = util.fetch_server_status(server["id"])
				except Exception as E:
					d[server["id"]] = {"error": str(E)}

		return jsonify(d)

	except Exception as E:
		return jsonify({"error": str(E)})


@bp_api.route("/stats/totals")
def page_api_stats_totals():
	try:
		return jsonify(util.fetch_server_totals())
	except Exception as E:
		return jsonify({"error": str(E)})

@bp_api.route("/playerlist")
def page_api_playerlist():
	try:
		d = {}

		for server in cfg.SERVERS:
			if server["open"]:
				try:
					d[server["id"]] = util.fetch_server_players(server["id"])
				except Exception as E:
					d[server["id"]] = {"error": str(E)}

		return jsonify(d)

	except Exception as E:
		return jsonify({"error": str(E)})

@bp_api.route("/playerlist/<string:id>")
def page_api_playerlist_server(id):
	if not util.get_server(id):
		return abort(404)

	try:
		return jsonify(util.fetch_server_players(id))
	except Exception as E:
		return jsonify({"error": str(E)})

@bp_api.route("/budget")
def page_api_budget():
	income = util.get_patreon_income()

	current_goal = min([goal for goal in cfg.WEBSITE['patreon-goals'] if goal > income] or (max(cfg.WEBSITE['patreon-goals']),)) # Find the lowest goal we haven't passed

	budget_stats = {
		"income": round(income/100, 2),
		"goal": round(current_goal/100, 2),
		"percent": int(income/current_goal*100)
	}
	return jsonify(budget_stats)


@bp_api.route("/stats/<string:id>")
def page_api_stats_server(id):
	if not util.get_server(id):
		return abort(404)

	try:
		return jsonify(util.fetch_server_status(id))
	except Exception as E:
		return jsonify({"error": str(E)})


@bp_api.route("/servers")
def page_api_servers():
	try:
		return jsonify(cfg.SERVERS)
	except Exception as E:
		return jsonify({"error": str(E)})


@bp_api.route("/linked_patreons")
def page_api_get_linked_patreons():
	if request.args.get("pass") == cfg.PRIVATE["api_passwd"]:
		try:
			return jsonify(db.site_db.query("SELECT patreon_id, ckey FROM patreon_link").fetchall())
		except Exception as E:
			return jsonify({"error": str(E)})
	else:
		return jsonify({"error": "bad pass"})


@bp_api.route("/bans")
def page_api_bans():
	try:
		ckey = request.args.get('ckey')
		if ckey:
			player = db.Player.from_ckey(ckey)
			if player:
				return jsonify(player.get_bans())
			else:
				return jsonify({"error": "Player not found!"})
		else:
			return jsonify({"error": "No Ckey Provided!"})
	except Exception as E:
		return jsonify({"error": "Unknown!"})