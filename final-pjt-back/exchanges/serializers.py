from rest_framework import serializers
from .models import Exchange,Country,Date

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = "__all__"

class ExchangeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Exchange
        fields = "__all__"
        read_only_fields = ('country','date')

class ExchangeListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    date = DateSerializer()
    class Meta:
        model = Exchange
        fields = "__all__"
