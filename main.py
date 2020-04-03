from flask import Flask, render_template, abort, flash, request, jsonify, send_file, redirect, session, Response
from elasticapm.contrib.flask import ElasticAPM
import os
import dbcl as db
import util

import patreon

import logging

import config as cfg

import math

import time

import datetime

import hashlib
import json

from flask_cors import CORS

app = Flask(__name__)

app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': cfg.PRIVATE["elastic"]["service-name"],
    'SECRET_TOKEN': cfg.PRIVATE["elastic"]["secret-token"],
	'SERVER_URL': cfg.PRIVATE["elastic"]["server-url"],
	'VERIFY_SERVER_CERT': False,
	'SERVER_CERT': '/srv/www/beesite/cert/instance.crt',
	'DEBUG': True
}

apm = ElasticAPM(app, logging=logging.ERROR)

@app.context_processor
def context_processor():
	return dict(cfg=cfg, db=db, util=util, session=dict(session))

@app.route("/")
def page_home():
	return render_template("home.html")

@app.route("/stats")
def page_stats():
	return render_template("stats.html")

@app.route("/rules/rp") # Temporary as I get crossed to update the rules urls everywhere
def page_rules_tempredirect():
	return redirect("/rules?server=rp")

@app.route("/rules")
def page_rules():
	alias = request.args.get('server', type=str, default="bee")
	server = util.get_server_from_alias(alias)

	if not server:
		return abort(404)

	return render_template("rules.html", rules=json.load(open("config/rules/{}.json".format(server["id"]))))

@app.route("/bans")
def page_bans():
	page = request.args.get('page', type=int, default=1)
	query = request.args.get('q', type=str, default="")

	response = db.game_db.get_bans((page-1)*cfg.WEBSITE["items-per-page"], page*cfg.WEBSITE["items-per-page"], query.lower().strip())

	bans = response[0]
	length = response[1]
	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]
	return render_template("bans.html", bans=bans, buttons=buttons, page=page, query=query, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))

@app.route("/library")
def page_library():
	page = request.args.get('page', type=int, default=1)
	response = db.game_db.get_library((page-1)*cfg.WEBSITE["items-per-page"], page*cfg.WEBSITE["items-per-page"])
	books = response[0]
	length = response[1]
	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]
	return render_template("library.html", books=books, buttons=buttons, page=page, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))

@app.route("/library/<int:bookid>")
def page_library_book(bookid):
	book = db.game_db.get_book(bookid)
	book["content"] = book["content"].replace("<font", "<font class=\"book-content\" color=")
	return render_template("book.html", book=book)


@app.route("/map")
def page_maps():
	return render_template("maps.html")

@app.route("/map/<string:map>")
def page_map(map):
	map_img = "/static/img/maps/{}.png".format(map)
	return render_template("map.html", map_img=map_img, map_name=map.title())

@app.route("/leaderboard")
def page_leaderboard():
	sort = request.args.get('sort', type=str, default='beecoins')
	lb = db.game_db.get_leaderboard(sort)
	return render_template("leaderboard.html", leaderboard=lb, sort=sort)

@app.route("/static/<string:d1>/<string:d2>")
def page_static(d1,d2):
	try:
		return send_file(os.path.join(".", "static", d1, d2))
	except:
		return abort(404)

@app.route("/favicon.ico")
def page_favicon():
	return send_file(os.path.join(".", "static", "img", "logo.png"))

@app.route("/api/stats")
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

@app.route("/api/stats/totals")
def page_api_stats_totals():
	try:
		return jsonify(util.fetch_server_totals())
	except Exception as E:
		return jsonify({"error": str(E)})

@app.route("/api/budget")
def page_api_budget():
	income = util.get_patreon_income()
	budget_stats = {
		"income": round(income/100, 2),
		"goal": round(cfg.WEBSITE['patreon-goal']/100, 2),
		"percent": int(income/cfg.WEBSITE['patreon-goal']*100)
	}
	return jsonify(budget_stats)


@app.route("/api/stats/<string:id>")
def page_api_stats_server(id):
	if not util.get_server(id):
		return abort(404)

	try:
		return jsonify(util.fetch_server_status(id))
	except Exception as E:
		return jsonify({"error": str(E)})


@app.route("/api/servers")
def page_api_servers():
	try:
		return jsonify(cfg.SERVERS)
	except Exception as E:
		return jsonify({"error": str(E)})


@app.route("/api/linked_patreons")
def page_api_get_linked_patreons():
	if request.args.get("pass") == cfg.PRIVATE["api_passwd"]:
		try:
			return jsonify(db.site_db.query("SELECT patreon_id, ckey FROM patreon_link").fetchall())
		except Exception as E:
			return jsonify({"error": str(E)})
	else:
		return jsonify({"error": "bad pass"})


@app.route("/api/bans")
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


@app.route("/join/<string:id>")
def page_join(id):
	try:
		server = util.get_server(id)
		return redirect("byond://{}:{}".format(server["host"],server["port"]))
	except Exception as E:
		pass


@app.route("/forum")
def page_forum():
	return redirect("https://forums.beestation13.com")


@app.route("/robots.txt")
@app.route("/Robots.txt")
def page_robotstxt():
	return send_file("static/Robots.txt")


@app.route("/sitemap.xml")
@app.route("/Sitemap.xml")
def page_sitemap():
	return send_file("static/sitemap.xml")



@app.route("/patreonauth")
def page_patreon_oauth():

	try:
		code = request.args.get('code')
		ckey = request.args.get('state')

		if code != None and ckey != None:
			oauth_client = patreon.OAuth(cfg.PRIVATE["patreon"]["client_id"], cfg.PRIVATE["patreon"]["client_secret"])

			tokens = oauth_client.get_tokens(code, 'https://beestation13.com/patreonauth')

			access_token = tokens['access_token']

			api_client = patreon.API(access_token)

			user_identity = api_client.get_identity().data()

			user_id = user_identity.id()

			player = db.Player.from_ckey(ckey)

			if not player:
				return redirect("/linkpatreon?error=invalidckey")
			
			db.site_db.link_patreon(ckey, user_id)

			return redirect("/linkpatreon?success=true")

		else:
			return redirect("/linkpatreon?error=unknown")

	except Exception as E:
		return str(E)
	
	return redirect("/linkpatreon?error=unknown")


@app.route("/linkpatreon")
def page_patreon_link():

	ckey = request.args.get("ckey")

	if ckey != None:

		player = db.Player.from_ckey(ckey)

		if player:
			return redirect("http://www.patreon.com/oauth2/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}&state={}".format(
				"code",
				cfg.PRIVATE["patreon"]["client_id"],
				"https://beestation13.com/patreonauth",
				"identity identity.memberships",
				str(ckey)
			))

		else:
			return redirect("/linkpatreon?error=invalidckey")

	return render_template("patreonlink.html")
