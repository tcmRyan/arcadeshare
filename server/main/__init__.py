from flask import Blueprint

main_bp = Blueprint(
    "main",
    __name__,
    static_url_path="/build",
    static_folder="../../frontend/build",
    template_folder="../../frontend/build",
)

from server.main import routes
