from django.urls import path
from .views import fetch_data, get_strike_option_expiry, get_symbols, get_expiry_for_symbol, index

urlpatterns = [ 
    path('', index, name='index'),
    path('data/', fetch_data, name='fetch-data'),
    path('symbols/', get_symbols, name='get-symbols'),
    path('expiry/', get_expiry_for_symbol, name='get-expiry'),
    path('strike/', get_strike_option_expiry, name='get-strike'),
]
