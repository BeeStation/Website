from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template
from flask import request

bp_leaderboard = Blueprint('leaderboard', __name__)

@bp_leaderboard.route("/leaderboard")
def page_leaderboard():
	lb = db.db_session.query(db.Player).order_by(db.Player.metacoins.desc())
	return render_template("leaderboard.html", leaderboard=lb)