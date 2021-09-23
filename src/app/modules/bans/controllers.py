from flask import Blueprint, render_template

from app import cfg, util

bp_bans = Blueprint("bans", __name__)


@bp_bans.route("/bans")
def page_bans():
    return render_template("bans.html")
