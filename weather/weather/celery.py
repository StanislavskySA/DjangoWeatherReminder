import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')
app = Celery('weather')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'record-weather-information-every-hour': {
        'task': 'cities.tasks.weather_data_to_db',
        'schedule': 3600.0,
    },
    'scan-subscribed-city': {
        'task': 'cities.tasks.subscribed_city_beat',
        'schedule': 1800.0,
    },
}
app.conf.timezone = 'UTC'
