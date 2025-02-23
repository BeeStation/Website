from flask import Blueprint
from flask import send_file

bp_meta = Blueprint("meta", __name__)


@bp_meta.route("/robots.txt")
@bp_meta.route("/Robots.txt")
def page_robotstxt():
    return send_file("static/Robots.txt")


@bp_meta.route("/sitemap.xml")
@bp_meta.route("/Sitemap.xml")
def page_sitemap():
    return send_file("static/sitemap.xml")


@bp_meta.route("/favicon.ico")
def page_favicon():
    return send_file("static/img/logo.png")
