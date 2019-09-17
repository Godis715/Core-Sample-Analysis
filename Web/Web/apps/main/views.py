from django.http import  Http404, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse
#from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')

