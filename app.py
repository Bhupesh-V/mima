from flask import Flask
import os, secrets
from . import db, auth

app = Flask(__name__, instance_relative_config=True)
# print(app.instance_path)
app.register_blueprint(auth.bp)
app.secret_key = secrets.token_urlsafe(16)
app.config["DATABASE"] = os.path.join(app.root_path, "mima.sqlite")

db.init_app(app)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
