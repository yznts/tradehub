from flask import Blueprint, render_template, redirect, request
import requests
import json
import collections

from src import settings
from src import auth

bp = Blueprint('table', __name__, template_folder="templates", static_folder="static")


@bp.route("/table/<game>")
@auth.requires_auth
def info(game):

    # Get services list
    services = collections.OrderedDict(sorted(json.loads(requests.get(settings.API_ADDR+"/services/available/"+game).text).items()))

    # Get items list
    items = collections.OrderedDict(json.loads(requests.get(settings.API_ADDR+"/items/all/"+game).text))

    # Last updates times
    last_updates = requests.get(settings.API_ADDR + "/services/last_updates/"+game).text

    # Extract params
    params = {
        "selected_services": request.args["services"].split(",") if "services" in request.args else [''],
        "s1_name": request.args["s1_name"] if "s1_name" in request.args else None,
        "s2_name": request.args["s2_name"] if "s2_name" in request.args else None,
        "s1_commission": request.args["s1_commission"] if "s1_commission" in request.args else None,
        "s2_commission": request.args["s2_commission"] if "s2_commission" in request.args else None,
        "price_target": request.args["price_target"] if "price_target" in request.args else None,
        "price_from": request.args["price_from"] if "price_from" in request.args else None,
        "price_to": request.args["price_to"] if "price_to" in request.args else None,
        "rates_s1_s2_from": request.args["rates_s1_s2_from"] if "rates_s1_s2_from" in request.args else None,
        "rates_s1_s2_to": request.args["rates_s1_s2_to"] if "rates_s1_s2_to" in request.args else None,
        "rates_s2_s1_from": request.args["rates_s2_s1_from"] if "rates_s2_s1_from" in request.args else None,
        "rates_s2_s1_to": request.args["rates_s2_s1_to"] if "rates_s2_s1_to" in request.args else None,
        "stattrack": request.args["stattrack"] if "stattrack" in request.args else "1"
    }

    # Table items
    fields = None
    table_items = []
    if params["selected_services"][0]:
        # Generate fields
        fields = ["Name"] + params["selected_services"]
        # Generate items price list for table
        for name, item_params in items.items():
            row = [[name, True]]
            for fname in params["selected_services"]:
                cname = services[fname]
                if cname + "-price" in item_params:
                    p = str(round(float(item_params[cname + "-price"]), 2))
                    av = item_params[cname + "-available"]
                    row.append([p, bool(int(av))])
                else:
                    row.append([0, False])
            table_items.append(row)

    # Table rates
    if params["s1_name"]:
        # Append fields
        if not fields:
            fields = ["Name", "S1->S2", "S2->S1"]
        else:
            fields.append("S1->S2")
            fields.append("S2->S1")
        # Get rates
        tparams = {
            "s1_name": params["s1_name"]
        }
        rates = json.loads(requests.get(settings.API_ADDR + "/rates/all/" + game, params=params).text)
        # Modify table
        for i in range(len(table_items)):
            name = table_items[i][0][0]
            if rates[name].get("s1-s2-rate") != 0 and rates[name].get("s2-s1-rate") != 0:
                s1_s2 = [round(rates[name]["s1-s2-rate"], 2), True]
                s2_s1 = [round(rates[name]["s2-s1-rate"], 2), True]
            else:
                s1_s2 = [0, False]
                s2_s1 = [0, False]
            table_items[i].append(s1_s2)
            table_items[i].append(s2_s1)

    # Filter items

    # Price
    if params["price_target"] and params["price_target"] in fields:
        field_index = fields.index(params["price_target"])
        remove_items = []
        for item in table_items:
            if not item[field_index][1]:
                remove_items.append(item)
                continue
            p = item[field_index][0]
            if float(p) < float(params["price_from"]) or float(p) > float(params["price_to"]):
                remove_items.append(item)
        for item in remove_items:
            table_items.remove(item)

    # Rates
    if params["rates_s1_s2_from"] and params["rates_s1_s2_to"] and "S1->S2" in fields:
        field_index = fields.index("S1->S2")
        remove_items = []
        for item in table_items:
            if not item[field_index][1]:
                remove_items.append(item)
                continue
            r = item[field_index][0]
            if float(r) < float(params["rates_s1_s2_from"]) or float(r) > float(params["rates_s1_s2_to"]):
                remove_items.append(item)
        for item in remove_items:
            table_items.remove(item)
    if params["rates_s2_s1_from"] and params["rates_s2_s1_to"] and "S2->S1" in fields:
        field_index = fields.index("S2->S1")
        remove_items = []
        for item in table_items:
            if not item[field_index][1]:
                remove_items.append(item)
                continue
            r = item[field_index][0]
            if float(r) < float(params["rates_s2_s1_from"]) or float(r) > float(params["rates_s2_s1_to"]):
                remove_items.append(item)
        for item in remove_items:
            table_items.remove(item)

    # StatTrack
    if params["stattrack"] and params["stattrack"] == "0":
        remove_items = []
        for item in table_items:
            if "StatTrak™" in item[0][0]:
                remove_items.append(item)
        for item in remove_items:
            table_items.remove(item)

    return render_template(
        "table.html",
        game=game,
        settings=settings,
        services=services,
        prev_params=params,
        fields=fields,
        table_items_price=table_items,
        last_updates=last_updates
    )