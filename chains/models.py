from datetime import date
from django.db import models

class Option(models.Model):
    symbol = models.CharField(max_length=30, null=True)
    expiration = models.DateField()
    strike_price = models.PositiveIntegerField(default=0)
    option_type = models.CharField(max_length=4)
    # expiration_type = models.CharField(max_length=8)


    def __str__(self):
        return "Symbol: %s, Expiration: %s, Strike: %s, OptionType: %s" % (self.symbol, self.expiration, self.strike_price, self.option_type)

    def save(self, *args, **kwargs):
        try:
            self.option_type = self.option_type
            option = Option.objects.get(strike_price=self.strike_price, expiration=self.expiration, option_type=self.option_type)
            return  # Don't save if found
        except self.DoesNotExist:
            super().save(*args, **kwargs)

class OptionPrice(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    ltp = models.FloatField(default=0.0)
    ltq = models.PositiveIntegerField(default=0)
    volume  = models.PositiveIntegerField(default=0)
    bid_price = models.FloatField(default=0.0)
    bid_qty = models.PositiveIntegerField(default=0)
    ask_price = models.FloatField(default=0.0)
    ask_qty = models.PositiveIntegerField(default=0)
    oi = models.PositiveIntegerField(default=0)
    prev_close = models.FloatField(default=0.0)
    prev_oi = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    streamtime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ltp} : {self.option}"


    def save(self, *args, **kwargs):
        try:
            optionPrice = OptionPrice.objects.get(
                ltp=self.ltp,
                ltq=self.ltq,
                volume=self.volume,
                bid_price=self.bid_price,
                bid_qty=self.bid_qty,
                ask_price = self.ask_price,
                ask_qty = self.ask_qty,
                oi=self.oi,
            )  # Don't save if found
        except self.DoesNotExist:
            super().save(*args, **kwargs)
