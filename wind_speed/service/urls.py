from django.urls import path

from .views import GeneralDataView, LocationDataView


urlpatterns = [
    path('general-data', GeneralDataView.as_view(), name='general-data'),
    path('location-data', LocationDataView.as_view(), name='location-data'),
]