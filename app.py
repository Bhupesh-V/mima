from flask import Flask
import os, secrets
from . import db, auth, post

app = Flask(__name__, instance_relative_config=True)

app.register_blueprint(auth.bp)
app.register_blueprint(post.bp)
app.add_url_rule("/", endpoint="index")

app.secret_key = secrets.token_urlsafe(16)

# 16 mb max size
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "/media")
app.config["DATABASE"] = os.path.join(app.root_path, "mima.sqlite")
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
