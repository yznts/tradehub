from functools import wraps
from flask import request, Response
import json
import dateparser
from datetime import datetime


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # Load users file
    with open("/var/users.json") as f:
        users = json.load(f)
    # Find user
    user = users.get(username)
    if not user:
        print("User not exists: ", user)
        return False
    # Check password
    if user.get("password") != password:
        print("Password incorrect")
        return False
    # Check expire date
    if dateparser.parse(user.get("expire"), settings={'DATE_ORDER': 'DMY'}) < datetime.now():
        print("Expired")
        return False

    return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated