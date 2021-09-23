from flask import Blueprint, render_template

from app import cfg, util

bp_index = Blueprint("index", __name__)


@bp_index.route("/")
def page_index():
    return render_template("home.html")
