from django.urls import path
from .views import WorkstationView

app_name = "workstation"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('', WorkstationView.as_view()),
]