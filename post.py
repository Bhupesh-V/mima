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

from auth import login_required
from db import get_db
from store import upload_image, purge_image
import os

bp = Blueprint("post", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, caption, body, created, author_id, username, likes, views"
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
                image_file_id = status["response"]["fileId"]

                db = get_db()
                db.execute(
                    "INSERT INTO post (caption, body, image_url, image_file_id, author_id)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (caption, body, image_url, image_file_id, g.user["id"]),
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
            "SELECT p.id, caption, body, created, author_id, username, name, views, image_url, image_file_id"
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
    db = get_db()
    is_already_liked = db.execute(
        "SELECT DISTINCT post_id, liker_id FROM likers WHERE post_id = ? AND liker_id = ?",
        (
            id,
            g.user["id"],
        ),
    ).fetchall()
    if len(is_already_liked) != 1:
        db.execute(
            "INSERT INTO likers (post_id, liker_id) VALUES (?, ?)",
            (
                id,
                g.user["id"],
            ),
        )
        db.execute("UPDATE post SET likes = likes + 1 WHERE id = ?", (id,))
        db.commit()
    return redirect(url_for("post.index"))


@bp.route("/post/<int:id>", methods=("GET",))
@login_required
def view(id):
    post = get_post(id, False)
    if post["author_id"] != g.user["id"]:
        db = get_db()
        db.execute("UPDATE post SET views = views + 1 WHERE id = ?", (id,))
        db.commit()
    return render_template("post/view.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = get_post(id)
    status = purge_image(post["image_file_id"])
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("post.index"))
