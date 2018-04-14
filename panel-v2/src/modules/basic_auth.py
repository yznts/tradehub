from functools import wraps
from flask import request, Response
import json
import datetime
import urllib.parse
import requests

from src.modules.config import config


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # Load user
    user = requests.get('{0}/openapi/user'.format(config.parent), params={
        'username': username,
        'password': password
    })
    user = json.loads(user.text)
    if not user:
        return False
    # Load sub
    sub = None
    for s in user['subs']:
        if s['sid'] == 1592:
            sub = s
    if not sub:
        return False
    # Check expire date
    expire = datetime.datetime.fromtimestamp(sub['expire']['$date']/1000)
    if expire < datetime.datetime.now():
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