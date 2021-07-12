from app import cfg
from app import util

from flask import Blueprint, render_template

bp_stats = Blueprint('stats', __name__)

@bp_stats.route("/stats")
def page_stats():
	return render_template("stats.html")
