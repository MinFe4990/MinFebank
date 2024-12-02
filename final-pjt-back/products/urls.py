from django.contrib import admin
from django.urls import path, include
from . import views
appname = "deposit"

urlpatterns = [
    path('deposit/',views.deposit),
    path('saving/',views.saving),
    path('banks/',views.banklist),
    path('sign/',views.sign),
    path('change/option/',views.changeOption),
]
