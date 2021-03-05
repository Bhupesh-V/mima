from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from mima.auth import login_required
from mima.db import get_db

bp = Blueprint("post", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, caption, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("post/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        caption = request.form["caption"]
        body = request.form["body"]
        image = request.files['file']
        error = None

        if not caption:
            error = "Caption is required."

        if error is not None:
            flash(error)
        else:
            image.save(secure_filename(image.filename))
            db = get_db()
            db.execute(
                "INSERT INTO post (caption, author_id)" " VALUES (?, ?)",
                (caption, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("post.index"))

    return render_template("post/create.html")


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("post.index"))
