from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    city_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_id}-{self.name}-{self.country}"


class CitiesWeather(models.Model):
    city_id = models.ForeignKey(City, on_delete=models.PROTECT)
    city = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    temperature_celcius = models.FloatField()
    humidity = models.IntegerField(default=0)
    weather = models.TextField(blank=True)
    icon = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}-{self.country_code}-{self.temperature_celcius}"


class Subscribed(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    remind_period = models.IntegerField()
    last_run_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}-{self.user}"
