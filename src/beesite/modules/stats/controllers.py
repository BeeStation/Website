from flask import Blueprint, render_template

from beesite import cfg, util

bp_stats = Blueprint("stats", __name__)


@bp_stats.route("/stats")
def page_stats():
    return render_template("stats.html")
