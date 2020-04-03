from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template
from flask import request

bp_leaderboard = Blueprint('leaderboard', __name__)

@bp_leaderboard.route("/leaderboard")
def page_leaderboard():
	sort = request.args.get('sort', type=str, default='beecoins')
	lb = db.game_db.get_leaderboard(sort)
	return render_template("leaderboard.html", leaderboard=lb, sort=sort)