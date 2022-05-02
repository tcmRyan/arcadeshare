from flask import current_app, redirect, url_for, render_template
from flask_security import login_required


@current_app.route("/")
def index():
    return redirect(url_for("main.app"))


@current_app.route('/admin-login')
@login_required
def admin_login():
    return redirect(url_for('security.login', next='/admin'))


@current_app.route("/app", defaults={"path": ""})
@current_app.route("/app/<path:path>")
def app(path):
    if "build" in path:
        filepath = path.spilt("build/")[1]
    return render_template("index.html")
