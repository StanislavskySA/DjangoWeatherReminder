import time
from celery import Celery
from django.core.mail import send_mail
from django.utils import timezone
from cities.models import City, Subscribed, CitiesWeather
from cities.views import get_weather

app = Celery()


@app.task
def weather_data_to_db():
    for city in City.objects.values_list('name',
                                         flat=True).distinct():
        get_weather(city)
        time.sleep(5)
        print(f'*** {city} weather data added ***')


@app.task
def subscribed_city_beat():
    subscribed_city = Subscribed.objects.all()
    for i in subscribed_city:
        td = timezone.now() - i.last_run_at
        hours = td.seconds // 3600
        if i.remind_period <= hours:
            w = CitiesWeather.objects.filter(city_id=i.city.id).last()
            last_weather_str = f'weather: {w.weather}\n' \
                               f'temp: {w.temperature_celcius}\n' \
                               f'humidity: {w.humidity}\n'
            send_mail(
                f'Weather notification for {i.city.name}',
                last_weather_str,
                'stas251977@gmail.com',
                [i.user.email],
                fail_silently=False,
            )
            i.last_run_at = timezone.now()
            i.save()
