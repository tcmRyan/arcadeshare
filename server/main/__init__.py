from flask import Blueprint

main_bp = Blueprint(
    "main",
    __name__,
    static_url_path="/build",
    static_folder="../../client/arcade/build",
    template_folder="../../client/arcade/build"
)

from server.main import routes
