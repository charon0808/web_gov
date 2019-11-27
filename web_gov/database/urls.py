from django.contrib import admin
from django.urls import path, re_path,include
from django.conf.urls import url

from . import views


urlpatterns = [
    path('get_all_table_names/', views.get_all_table_names),
    path('get_table_sample/', views.get_table_sample),
    path('write_table_content/', views.write_table_content),
    path('update_table_content/', views.update_table_content)
]
