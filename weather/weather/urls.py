"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from cities.views import CitiesWeatherAPIList, SubscribedAPIList
from cities.views import CityAPIList
from cities.views import SubscribedAPIDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/weather-auth/', include('rest_framework.urls')),
    path('api/citiesweather/', CitiesWeatherAPIList.as_view(),
         name='weather'),
    path('api/cities/', CityAPIList.as_view(), name='city'),
    path('api/subscribed/', SubscribedAPIList.as_view(), name='subscribed'),
    path('api/subscribed_delete_update/<int:pk>/',
         SubscribedAPIDetailView.as_view(), name='subscribed_update'),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]
