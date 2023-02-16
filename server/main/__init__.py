from flask import Blueprint

main_bp = Blueprint(
    "main",
    __name__,
    static_url_path="/build",
    static_folder="../../client/build",
    template_folder="../../client/build"
)

from server.main import routes
