from django.contrib import admin
from django.urls import path, re_path,include
from django.conf.urls import url

from . import views


urlpatterns = [
    path('get_all_algorithm_names/', views.algorithm_names),
    path('get_all_jobs/', views.running_jobs),
    path('show_details/', views.show_details),
    path('run/', views.run),
]
