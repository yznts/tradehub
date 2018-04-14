from flask import Flask

from src.modules.config import config


# Init
app = Flask(__name__)

# Config
app.debug = config.debug
app.secret_key = config.secret


if __name__ == '__main__':
    app.run()
