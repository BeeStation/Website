from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template

bp_maps = Blueprint('maps', __name__)

@bp_maps.route("/map")
def page_maps():
	return render_template("maps.html")


@bp_maps.route("/map/<string:map>")
def page_map(map):
	map_img = "/static/img/maps/{}.png".format(map)
	return render_template("map.html", map_img=map_img, map_name=map.title())
