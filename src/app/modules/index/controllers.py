from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template

bp_index = Blueprint('index', __name__)

@bp_index.route("/")
def page_index():
	return render_template("home.html")