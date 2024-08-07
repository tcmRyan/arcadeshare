import os
from flask import current_app, redirect, url_for, send_from_directory
from flask_security import login_required

from src.server.main import main_bp


@current_app.route("/")
def index():
    return redirect(url_for("main.app"))


@main_bp.route("/", defaults={"path": ""})
@main_bp.route("/<path:path>")
def app(path):
    if path != "" and os.path.exists(main_bp.static_folder + '/' + path):
        return send_from_directory(main_bp.static_folder, path)
    else:
        return send_from_directory(main_bp.static_folder, 'index.html')
