from django.contrib import admin

# Register your models here.

from .models import CitiesWeather, City, Subscribed

admin.site.register(CitiesWeather)
admin.site.register(City)
admin.site.register(Subscribed)
