from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('E-courses app')

def welcome(request): 
    return HttpResponse("Hello")