from flask import Blueprint, send_from_directory


bp = Blueprint('static', __name__, template_folder="templates", url_prefix="/static", static_folder="static")


@bp.route("/<path:path>")
def static_page(path):
    return send_from_directory(".", path)