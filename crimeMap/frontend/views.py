from django.shortcuts import render
from django.http import HttpResponse
from .models import Callinfo
from .models import Arrestinfo 

# Create your views here.
def helloWorldView(request):
    return HttpResponse("Hello World")

def mapView(request):
    callBlotter = Callinfo.objects.filter(latitude__isnull = False).order_by("-cfs_number")[:1000]
    context = {
        "callBlotter":callBlotter
    }
    return render(request, "map.html", context)

def simpleCrimeListView(request):
    callBlotter = Callinfo.objects.order_by("-cfs_number")[:100]
    context = {
        "callBlotter":callBlotter
    }
    return render(request, "simpleTable.html", context)