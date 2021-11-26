from django.db import models
from django.db.models import fields


class RssItem(models.Model):
    description =  fields.CharField(max_length=1024) # Usually description items have around 250 chars
    guid = fields.CharField(max_length=36)
    link = fields.CharField(max_length=256)
    date = fields.DateField()
    title = fields.CharField(max_length=256)
    symbol = models.CharField(max_length=5) # Found that tickers can go up to 5 characters