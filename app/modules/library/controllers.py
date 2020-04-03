from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template
from flask import request

import math

bp_library = Blueprint('library', __name__)

@bp_library.route("/library")
def page_library():
	page = request.args.get('page', type=int, default=1)
	response = db.game_db.get_library((page-1)*cfg.WEBSITE["items-per-page"], page*cfg.WEBSITE["items-per-page"])
	books = response[0]
	length = response[1]
	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]
	return render_template("library.html", books=books, buttons=buttons, page=page, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))


@bp_library.route("/library/<int:bookid>")
def page_library_book(bookid):
	book = db.game_db.get_book(bookid)
	book["content"] = book["content"].replace("<font", "<font class=\"book-content\" color=")
	return render_template("book.html", book=book)
