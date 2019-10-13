from django.urls import path, include
from . import views

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    # path('', ''),
    path('upload', views.upload, name="upload"),
    # path('analyse/<string:csId>', ''),
    # path('status', ''),
]