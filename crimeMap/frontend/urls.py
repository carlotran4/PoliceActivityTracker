from django.urls import path
from .views import helloWorldView
from .views import simpleCrimeListView
urlpatterns = []

urlpatterns += [path("", helloWorldView, name="helloworld")]
urlpatterns += [path("listing", simpleCrimeListView, name = "listing")]