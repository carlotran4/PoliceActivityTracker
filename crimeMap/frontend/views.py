from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def helloWorldView(request):
    return HttpResponse("Hello World")

def simpleCrimeListView(request):
    return HttpResponse("Simple Crime List View")