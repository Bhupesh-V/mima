from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from mima.auth import login_required
from mima.db import get_db
from mima.store import upload_image
import os

bp = Blueprint("post", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, caption, hashtags, created, author_id, username, likes"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("post/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        caption = request.form["caption"]
        tags = request.form["hashtags"]
        image = request.files["file"]
        error = None

        if not caption:
            error = "Caption is required."

        if error is not None:
            flash(error)
        else:
            imagepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], secure_filename(image.filename)
            )
            imagename = secure_filename(image.filename)
            image.save(imagepath)
            # upload image to imagekit
            status = upload_image(imagepath, imagename)
            if status["error"] is None:
                image_url = status["response"]["url"]

                db = get_db()
                db.execute(
                    "INSERT INTO post (caption, hashtags, image_url, author_id)"
                    " VALUES (?, ?, ?, ?)",
                    (caption, tags, image_url, g.user["id"]),
                )
                db.commit()
                return redirect(url_for("post.index"))
            else:
                abort(500, "File Upload Error")

    return render_template("post/create.html")


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, caption, hashtags, created, author_id, username, image_url"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/post/<int:id>", methods=("POST",))
@login_required
def like(id):
    get_post(id, False)
    db = get_db()
    db.execute("UPDATE post SET likes = likes + 1 WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("post.index"))


@bp.route("/post/<int:id>", methods=("GET",))
@login_required
def view(id):
    post = get_post(id, False)
    return render_template("post/view.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("post.index"))
