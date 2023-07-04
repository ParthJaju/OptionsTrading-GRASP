from django.contrib import admin
from .models import Option,OptionPrice

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'expiration', 'strike_price', 'option_type']
    list_filter = ['symbol', 'option_type', 'strike_price']


@admin.register(OptionPrice)
class OptionPriceAdmin(admin.ModelAdmin):
    list_display = ['option', 'ltp' ]
    list_filter = ['option__symbol', 'option__option_type', 'option__strike_price']
