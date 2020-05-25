from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

import math

bp_bans = Blueprint('bans', __name__)

@bp_bans.route("/bans")
def page_bans():
	page = request.args.get('page', type=int, default=1)
	query = request.args.get('q', type=str, default="")

	json_format = request.args.get('json', type=int, default=0)

	page = max(min(page, 1000000), 1) # Arbitrary number. We probably won't ever have to deal with 1,000,000 pages of bans. Hopefully..

	response = db.game_db.get_bans((page-1)*cfg.WEBSITE["items-per-page"], page*cfg.WEBSITE["items-per-page"], query.lower().strip())

	bans = response[0]
	length = response[1]
	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]

	if json_format:
		return jsonify(bans)

	return render_template("bans.html", bans=bans, buttons=buttons, page=page, query=query, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))
