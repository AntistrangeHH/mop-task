from django.db.models import fields
from rest_framework import serializers
from .models import RssItem
from rest_framework.pagination import PageNumberPagination

# Serialie the model on all fields
class RssItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = RssItem
        fields = '__all__'
