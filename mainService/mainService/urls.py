"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import login, logout

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/login', login),
    path('api/logout', logout),
    path('api/core_sample/', include('core_sample.urls')),
    path('api/workstation/', include('workstation.urls')),
    path('admin/', admin.site.urls),
]

# Added the url of static files. For example: /static/core_sample/user_USERNAME/cs_UUID/FILENAME
urlpatterns += staticfiles_urlpatterns()
