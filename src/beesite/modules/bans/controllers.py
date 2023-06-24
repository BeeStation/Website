from flask import Blueprint
from flask import render_template

bp_bans = Blueprint("bans", __name__)


@bp_bans.route("/bans")
def page_bans():
    return render_template("bans.html")
