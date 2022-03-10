from rest_framework import serializers
from .models import CitiesWeather, City, Subscribed


class CitiesWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitiesWeather
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class SubscribedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribed
        fields = "__all__"
