from django.utils import timezone
from rest_framework import generics
import requests
import csv
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from weather.settings import WEATHER_PASS_KEY
from .models import CitiesWeather, City, Subscribed
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import CitiesWeatherSerializer, CitySerializer
from .serializers import SubscribedSerializer

# Create your views here.


class CitiesWeatherAPIList(generics.ListCreateAPIView):
    queryset = CitiesWeather.objects.all()
    serializer_class = CitiesWeatherSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        cities = list(City.objects.filter(
            subscribed__user_id=self.request.user.id).values_list(
            'name', flat=True))
        return CitiesWeather.objects.filter(city__in=cities)


class CityAPIList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)


class SubscribedAPIList(generics.ListCreateAPIView):
    queryset = Subscribed.objects.all()
    serializer_class = SubscribedSerializer
    permission_classes = (IsAuthenticated,)


class SubscribedAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscribed.objects.all()
    serializer_class = SubscribedSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


def get_weather(city):
    api_key = WEATHER_PASS_KEY
    url = 'https://api.weatherbit.io/v2.0/current?city={}&key={}'
    result = requests.get(url.format(city, api_key))
    city_id = City.objects.filter(city=city)
    if result:
        json = result.json()
        city = json['data'][0]['city_name']
        country_code = json['data'][0]['country_code']
        temperature_celcius = json['data'][0]['temp']
        humidity = json['data'][0]['rh']
        weather = json['data'][0]['weather']['description']
        icon = json['data'][0]['weather']['icon']

        city_weather_obj, created = CitiesWeather.objects.update_or_create(
            city_id=city_id.id,
            city=city,
            country_code=country_code,
            temperature_celcius=temperature_celcius,
            humidity=humidity,
            weather=weather,
            icon=icon,
            updated=timezone.now(),
            defaults={'city': "Dubai"},
        )
        city_weather_obj.save()


def import_cities_csv():
    """The function is run once to write sities data to"""
    """the database from a real *.csv file"""
    with open("cities_mini.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        for row in file_reader:
            city_data = City.objects.create(
                city_id=row["city_id"],
                name=row["city_name"],
                country=row["country_full"],
            )
            city_data.save()
