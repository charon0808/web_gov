from django.contrib import admin
from django.urls import path, re_path,include
from django.conf.urls import url

from . import views


urlpatterns = [
    path('get_all_algorithm_names/', views.algorithm_names),
    path('run/', views.run),
]
