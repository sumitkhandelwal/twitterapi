from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views
from .views import userinput

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse/', views.analyse, name='analyse')
]