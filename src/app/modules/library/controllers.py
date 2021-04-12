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

	query = db.db_session.query(db.Book).order_by(db.Book.datetime.desc())

	length = query.count()

	displayed_books = query.offset((page-1)*cfg.WEBSITE["items-per-page"]).limit(page*cfg.WEBSITE["items-per-page"])
	
	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]
	return render_template("library.html", books=displayed_books, buttons=buttons, page=page, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))


@bp_library.route("/library/<int:bookid>")
def page_library_book(bookid):
	book = db.Book.from_id(bookid)
	return render_template("book.html", book=book)
