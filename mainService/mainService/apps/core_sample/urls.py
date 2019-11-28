from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

import uuid

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    # GET api/core_sample/
    path('', views.cs_getAll, name="cs_getAll"),
    # GET api/core_sample/<uuid:csId>
    path('<uuid:csId>/', views.cs_get, name="cs_get"),
    # DELETE api/core_sample/<uuid:csId>/delete <-- * '/delete' is the temporary decision *
    path('<uuid:csId>/delete/', views.cs_delete, name="cs_delete"),
    # PUT api/core_sample/<uuid:csId>/analyse
    path('<uuid:csId>/analyse/', views.cs_analyse, name="cs_analyse"),
    # GET api/core_sample/<uuid:csId>/markup
    path('<uuid:csId>/markup/', views.cs_markup_get, name="cs_markup_get"),
    # PUT api/core_sample/<uuid:csId>/markup/put <-- * '/put' is the temporary decision *
    path('<uuid:csId>/markup/put/', views.cs_markup_put, name="cs_markup_put"),
    # POST api/core_sample/upload
    path('upload/', views.cs_upload, name="cs_upload"),
    # PUT api/core_sample/status
    path('status/', views.css_status, name="css_status"),
    # PUT api/core_sample/statistics/
    path('statistics/', views.css_statistics, name="css_statistics"),
    path('status/', views.css_status, name="css_status"),
]

