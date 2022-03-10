"""Models Testing"""


class TestModel(TestCase):
    def setUp(self):
        test = User.objects.create(username='test', first_name='test')
        city = City.objects.create(city_id=292223, name='Dubai', country='AE')
        subscribed_city = Subscribed.objects.create(user=test,
                                                    city=city,
                                                    remind_period=1
                                                    )
        weather = CitiesWeather.objects.create(
            city='Dubai',
            country_code='AE',
            temperature_celcius=30,
            humidity=80,
            weather='Clear',
            icon='c02n',
        )

    def tearDown(self):
        pass

    def test_city_name_label(self):
        city = City.objects.first()
        field_label = city._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_weather_name_label(self):
        weather = CitiesWeather.objects.first()
        field_label = weather._meta.get_field('weather').verbose_name
        self.assertEquals(field_label, 'weather')

    def test_object_id(self):
        subscribed_city = Subscribed.objects.get(id=1)
        city = City.objects.get(id=1)
        self.assertEquals(subscribed_city.city, city)