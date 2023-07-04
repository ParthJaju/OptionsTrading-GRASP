import re
from datetime import datetime
import pandas as pd

from django.shortcuts import render
from django.utils import dateparse
from .models import Option, OptionPrice
# Create your views here.

def extract_symbol_components(symbol):
    expiry_match = re.search(r'(\d{2})([A-Za-z]{3})(\d{2})(\d+)([A-Za-z]+)', symbol)
    if expiry_match:
        expiry_day = expiry_match.group(1)
        expiry_month = expiry_match.group(2)
        expiry_year = expiry_match.group(3)
        expiry = expiry_day + ' ' + expiry_month + ' ' + expiry_year
        strike_price = expiry_match.group(4)
        put_call = expiry_match.group(5)
        name_match = re.search(r'^([A-Za-z]+)', symbol)
        name = name_match.group(1) if name_match else None
        return name, expiry, strike_price, put_call
    else:
        return None, None, None, None

def fetch_data(request):
    df = pd.read_csv('dataset.csv')
    arr = df['MAINIDX'].unique()
    for i in arr:
        name, expiry, strike_price, put_call = extract_symbol_components(i)
        price = 0.0
        if expiry and strike_price:
            expiry = datetime.strptime(expiry, '%d %b %y').date()
            price = float(strike_price)
            option = Option.objects.create(
                symbol=name,
                expiration=expiry, 
                strike_price=price, 
                option_type=put_call
            )


def get_symbols():
    options = Option.objects.all()
    context = {'options': options}
    context['symbols'] = set(options.values_list('symbol', flat=True))
    return context['symbols']

def get_expiry_for_symbol(request):
    if request.method == 'POST':
        data = request.POST
        symbols = get_symbols()
        symbol = data.get("symbol")
        exp = data.get("expiry")
        strike = data.get("strike")
        if exp and strike:
            strike = None
        context = {}
        options = Option.objects.filter(symbol=symbol)
        context['expiry'] = list(set(options.values_list('expiration', flat=True)))
        context['strikes'] = list(set(options.values_list('strike_price', flat=True)))
        if strike:
            context['strike_price'] = int(strike)
        context['symbols'] = symbols
        context['sym'] = symbol
        context['expiration'] = exp
        strikes = context['strikes']
        strikes.sort()

        unique_options = Option.objects.none()
        if exp and not strike:
            for strk in strikes:
                option = Option.objects.filter(strike_price=strk, symbol=symbol).first()
                unique_options = unique_options | Option.objects.filter(pk=option.pk)
        elif strike:
            for e in context['expiry']:
                option = Option.objects.filter(expiration=e, symbol=symbol).first()
                unique_options = unique_options | Option.objects.filter(pk=option.pk)

        if exp and not strike:
            exp = datetime.strptime(exp, "%d %b %Y").date()
            unique_options = unique_options.filter(expiration=exp)
        elif strike:
            unique_options = unique_options.filter(strike_price=strike)

        context['option_prices'] = list()
        optionprices = OptionPrice.objects.filter(option__symbol=symbol).select_related('option')
        options = unique_options

        for option in options:
            option_price = {
                "call": optionprices.filter(
                    option__strike_price=option.strike_price,
                    option__option_type="CE"
                ).order_by('-timestamp').first(),
                "put": optionprices.filter(
                    option__strike_price=option.strike_price, 
                    option__option_type="PE"
                ).order_by('-timestamp').first(),
                'strike': option.expiration.strftime("%d %b %Y") if not exp and strike else option.strike_price,
            }
            context['option_prices'].append(option_price)
        return render(request, 'expiry_list.html', context)
    else:
        context = {}
        data = request.GET
        symbol = data.get('symbol')
        expiry = data.get('expiry')
        strike = data.get("strike")
        if strike and expiry:
            strike = None
        if strike:
            context['strike_price'] = int(strike)
        if expiry:
            exp = datetime.strptime(expiry, "%d %b %Y").date()
        else:
            exp = ""
        options = Option.objects.filter(symbol=symbol)
        context['strikes'] = list(set(options.values_list('strike_price', flat=True)))
        context['expiry'] = list(set(options.values_list('expiration', flat=True)))
        strikes = context['strikes']
        strikes.sort()
        unique_options = Option.objects.none()
        for strk in strikes:
            option = Option.objects.filter(strike_price=strk, symbol=symbol).first()
            unique_options = unique_options | Option.objects.filter(pk=option.pk)
        if exp and not strike:
            unique_options = unique_options.filter(expiration=exp)
        elif strike:
            unique_options = unique_options.filter(strike_price=strike)

        context['sym'] = symbol
        context['expiration'] = expiry
        context['option_prices'] = list()
        optionprices = OptionPrice.objects.filter(option__symbol=symbol).select_related('option')
        options = unique_options

        for option in options:
            option_price = {
                "call": optionprices.filter(
                    option__strike_price=option.strike_price,
                    option__option_type="CE"
                ).order_by('-timestamp').first(),
                "put": optionprices.filter(
                    option__strike_price=option.strike_price, 
                    option__option_type="PE"
                ).order_by('-timestamp').first(), 
                'strike': option.expiration.strftime("%d %b %Y") if not exp and strike else option.strike_price,
            }
            context['option_prices'].append(option_price)
        return render(request, 'table.html', context)


def get_strike_option_expiry(request):
    context = {}
    data = request.POST
    symbols = get_symbols()
    symbol=data.get("symbol")
    expiry = data.get("expiry")
    expiry = dateparse.parse_date(expiry)
    options = Option.objects.filter(symbol=symbol, expiration=expiry)
    context['strike'] = set(options.values_list('strike_price', flat=True))
    return render(request, 'expiry_list.html', context)

def index(request):
    symbols = get_symbols()
    context = {'symbols': symbols,}
    return render(request, 'index.html', context)

