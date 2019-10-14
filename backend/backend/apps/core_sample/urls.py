from django.urls import path, include
from . import views

app_name = "core_sample"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    #path('', ''),
    path('<uuid:csId>', views.delete, name="delete"),
    path('upload', views.upload, name="upload"),
    # path('analyse/<string:csId>', ''),
    # path('analyse/<string:csId>', ''),
    # path('status', ''),
]