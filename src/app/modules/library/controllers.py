from flask import Blueprint, render_template

from app import cfg, util

bp_library = Blueprint("library", __name__)


@bp_library.route("/library")
def page_library():
    return render_template("library.html")


@bp_library.route("/library/<int:book_id>")
def page_library_book(book_id):
    return render_template("book.html", book_id=book_id)
