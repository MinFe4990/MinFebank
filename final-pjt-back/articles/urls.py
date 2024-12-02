
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.articleControl),
    path("detail/",views.articledetail),
    path("detail/like/",views.articleLike),
    path("commit/",views.commit),
]