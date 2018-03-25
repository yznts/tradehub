from flask import Blueprint, render_template, redirect
import requests
import json
import collections

from src import settings

bp = Blueprint('info', __name__, template_folder="templates", static_folder="static")

@bp.route("/")
def index():
    return redirect("/info")

@bp.route("/info")
def info():

    # Get available games
    r = requests.get(settings.API_ADDR+"/services/games")
    games = json.loads(r.text)

    # Get services and items count for each game
    icount = {}
    for g in games:
        r = requests.get(settings.API_ADDR+"/services/items_count/"+g)
        data = json.loads(r.text)
        icount[g] = collections.OrderedDict(sorted(data.items()))

    # Sort for only one possible layout
    icount = collections.OrderedDict(sorted(icount.items()))

    return render_template("info.html", icount=icount)
