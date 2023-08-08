from django.urls import path
from .views import mapView
from .views import simpleCrimeListView
urlpatterns = []

urlpatterns += [path("", mapView, name="map")]
urlpatterns += [path("listing", simpleCrimeListView, name = "listing")]