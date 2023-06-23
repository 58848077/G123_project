from django.db import models

class financial_data(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    symbol = models.CharField(max_length=20)
    date = models.CharField(max_length=10)
    open_price = models.FloatField(default=0)
    close_price = models.FloatField(default=0)
    volume = models.IntegerField(default=0)

    class Meta:
        unique_together = ('symbol', 'date')
        app_label = 'fin_data'
