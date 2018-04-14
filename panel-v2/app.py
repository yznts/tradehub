from flask import Flask, g
from flask_debugtoolbar import DebugToolbarExtension
import datetime
import time

from src.modules.config import config


# Init
app = Flask(__name__)

# Config
app.debug = config.debug
app.secret_key = config.secret

# Extensions
if config.debug:
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    toolbar = DebugToolbarExtension(app)


# Jinja add-ons
@app.before_request
def before_request():
    g.config = config
    g.request_start_time = time.time()
    g.request_time = lambda: "%.3fs" % (time.time() - g.request_start_time)


@app.template_filter('ctime')
def timectime(s):
    dt = datetime.datetime.fromtimestamp(s)
    return dt.strftime('%d-%m-%Y %H:%M')


# Connect blueprints
import src.controllers.static
import src.controllers.index
import src.controllers.table

app.register_blueprint(src.controllers.static.bp)
app.register_blueprint(src.controllers.index.bp)
app.register_blueprint(src.controllers.table.bp, url_prefix='/table')


if __name__ == '__main__':
    app.run()
