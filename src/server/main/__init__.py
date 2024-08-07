from flask import Blueprint

main_bp = Blueprint(
    "main",
    __name__,
    static_url_path="/build",
    static_folder="./build",
    template_folder="./build",
)

from src.server.main import routes
