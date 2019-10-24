from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

import uuid

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('', views.cs_getAll, name="cs_getAll"),
    path('<uuid:csId>', views.cs_get, name="cs_get"),
    path('<uuid:csId>/delete', views.cs_delete, name="cs_delete"),
    path('<uuid:csId>/analyse', views.cs_analyse, name="cs_analyse"),
    path('<uuid:csId>/markup', views.cs_markup_get, name="cs_markup_get"),
    # path('<uuid:csId>/markup', views.cs_markup_put, name="cs_markup_put"),
    path('upload', views.cs_upload, name="cs_upload"),
    path('status', views.css_status, name="css_status"),
]

