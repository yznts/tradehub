from flask import Blueprint, render_template, request
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
import requests
import json

from src.modules.config import config
from src.modules.basic_auth import requires_auth

bp = Blueprint('table', __name__)


@bp.route('/<game>', methods=['GET', 'POST'])
@requires_auth
def table(game):

    datatable = {}

    # Load items cache
    cache = requests.get('{0}/get'.format(config.cache_layer_address), params={
        'api_key': config.cache_layer_api_key,
        'path': game
    })
    items = json.loads(cache.text)

    # Extract markets
    markets = set()
    for item_name, item_fields in items.items():
        for field, value in item_fields.items():
            markets.add(field.split('|')[0])
    markets = list(sorted(markets))

    # GET request backport
    form = MultiDict(request.form)
    if request.args.get('services'):
        for s in request.args.get('services').split(','):
            form.add('markets', s)
    if request.args.get('s1_name') and request.args.get('s2_name') and request.args.get('s1_commission') and request.args.get('s2_commission'):
        form.add('rates-s1', request.args.get('s1_name'))
        form.add('rates-s2', request.args.get('s2_name'))
        form.add('rates-s1-commission', request.args.get('s1_commission'))
        form.add('rates-s2-commission', request.args.get('s2_commission'))
    if request.args.get('price_target'):
        form.add('filters-price-target', request.args.get('price_target'))
    if request.args.get('price_from'):
        form.add('filters-price-from', request.args.get('price_from'))
    if request.args.get('price_to'):
        form.add('filters-price-to', request.args.get('price_to'))

    
    request.form = ImmutableMultiDict(form)

    # Table processing
    if request.method == 'POST':

        # Rates
        rates_flag = False
        if request.form.get('rates-s1') and request.form.get('rates-s2') and \
            request.form.get('rates-s1-commission') and request.form.get('rates-s2-commission'):
            
            rates_flag = True

            s1 = request.form.get('rates-s1')
            s2 = request.form.get('rates-s2')
            s1_commission = 1-(float(request.form.get('rates-s1-commission'))/100)
            s2_commission = 1-(float(request.form.get('rates-s2-commission'))/100)

            for item_name in items:
                s1_price = items[item_name].get('{0}|price'.format(s1)) or 0
                s2_price = items[item_name].get('{0}|price'.format(s2)) or 0

                s1_price_ac = s1_price * s1_commission
                s2_price_ac = s2_price * s2_commission

                items[item_name]['s12r'] = 100-((s1_price/s2_price_ac)*100) if s1_price and s2_price else 0
                items[item_name]['s21r'] = ((s1_price_ac/s2_price)*100)-100 if s1_price and s2_price else 0


        # Filters
        if request.form.get('filters-price-target') and request.form.get('filters-price-from'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                price = item_fields.get('{0}|price'.format(request.form.get('filters-price-target'))) or 0
                if price > float(request.form.get('filters-price-from')):
                    filtered_items[item_name] = item_fields
            items = filtered_items
        if request.form.get('filters-price-to') and request.form.get('filters-price-to'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                price = item_fields.get('{0}|price'.format(request.form.get('filters-price-target'))) or 0
                if price < float(request.form.get('filters-price-to')):
                    filtered_items[item_name] = item_fields
            items = filtered_items
        if rates_flag and request.form.get('filters-rates-s12-from'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                s12r = item_fields.get('s12r')
                if s12r > float(request.form.get('filters-rates-s12-from')):
                    filtered_items[item_name] = item_fields
            items = filtered_items
        if rates_flag and request.form.get('filters-rates-s21-from'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                s12r = item_fields.get('s21r')
                if s12r > float(request.form.get('filters-rates-s21-from')):
                    filtered_items[item_name] = item_fields
            items = filtered_items
        if rates_flag and request.form.get('filters-rates-s12-to'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                s12r = item_fields.get('s12r')
                if s12r < float(request.form.get('filters-rates-s12-to')):
                    filtered_items[item_name] = item_fields
            items = filtered_items
        if rates_flag and request.form.get('filters-rates-s21-to'):
            filtered_items = {}
            for item_name, item_fields in items.items():
                s12r = item_fields.get('s21r')
                if s12r < float(request.form.get('filters-rates-s21-to')):
                    filtered_items[item_name] = item_fields
            items = filtered_items

        # Table generate
        datatable['columns'] = [{'title': 'Name', 'type': 'text', 'width': 1000}] + [{'title': x, 'type': 'number', 'width': 0} for x in request.form.getlist('markets')]
        if rates_flag: datatable['columns'].append({'title': 'S1->S2', 'type': 'number', 'width': 0})
        if rates_flag: datatable['columns'].append({'title': 'S2->S1', 'type': 'number', 'width': 0})
        datatable['data'] = []
        for item_name, item_fields in items.items():
            dt_row = []
            for dt_column in datatable['columns']:
                if dt_column['title'] == 'Name':
                    dt_row.append(json.dumps({'val': item_name, 'type': 'text', 'class': '', 'copy': True}))
                elif dt_column['title'] == 'S1->S2':
                    dt_row.append(json.dumps({
                        'val': item_fields.get('s12r'),
                        'type': 'percent',
                        'class': '' if item_fields.get('s12r') != 0 else 'not-av'
                    }))
                elif dt_column['title'] == 'S2->S1':
                    dt_row.append(json.dumps({
                        'val': item_fields.get('s21r'),
                        'type': 'percent',
                        'class': '' if item_fields.get('s21r') != 0 else 'not-av'
                    }))
                else:
                    dt_row.append(json.dumps({
                        'val': item_fields.get('{0}|price'.format(dt_column['title'])) or 0,
                        'type': 'price',
                        'class': '' if item_fields.get('{0}|available'.format(dt_column['title'])) else 'not-av',
                        'link': item_fields.get('{0}|link'.format(dt_column['title']))
                    }))
            datatable['data'].append(dt_row)

        

    return render_template('table.html', game=game, form=request.form, markets=markets, datatable=json.dumps(datatable))
