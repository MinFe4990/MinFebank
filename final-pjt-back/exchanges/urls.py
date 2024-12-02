
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.exchangelist),
    ## data에 range 항목을 보내면 해당 범위만큼 데이터를 가져온다.
    path("country/",views.country)
]
