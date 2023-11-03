from django.urls import path

from .views import GeneralDataView, LocationDataView


urlpatterns = [
    path('location-data', LocationDataView.as_view(), name='location-data'),
]