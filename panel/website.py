from flask import Flask, g
import time

from src import settings

print("WEB:\t ", settings.WEB_VER)
print("CORE:\t ", settings.CORE_VER)
print("PLUGIN:\t ", settings.PLUGIN_VER)

import src.controllers.static
import src.controllers.info
import src.controllers.table

blueprints = [
    src.controllers.static.bp,
    src.controllers.info.bp,
    src.controllers.table.bp,
]

app = Flask(__name__)

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

for b in blueprints:
    print(b.name, b.url_prefix)
    app.register_blueprint(b)

if __name__ == '__main__':
    app.run(host='0.0.0.0')