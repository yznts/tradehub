import flask

bp = flask.Blueprint('static', __name__)


@bp.route('/<path:path>')
def static_files(path):
    return flask.send_from_directory('static', path)
