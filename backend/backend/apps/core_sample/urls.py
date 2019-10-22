from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

import uuid

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('', views.getAll, name="getAll"),
    path('<uuid:csId>', views.get, name="get"),
    path('delete/<uuid:csId>', views.delete, name="delete"),
    path('upload', views.upload, name="upload"),
    path('analyse/<uuid:csId>', views.analyse, name="analyse"),
    path('status', views.status, name="status"),
]

