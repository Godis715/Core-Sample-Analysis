from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

import uuid

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('', views.cs_getAll, name="getAll"),
    path('<uuid:csId>', views.cs_get, name="get"),
    path('<uuid:csId>/delete', views.delete, name="delete"),
    path('<uuid:csId>/analyse', views.analyse, name="analyse"),
    path('upload', views.upload, name="upload"),
    path('status', views.status, name="status"),
]

