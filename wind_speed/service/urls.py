from django.urls import path

from .views import LocationDataView, LocationMonthDataView


urlpatterns = [
    path('localidad/<str:tipo>', LocationDataView.as_view(), name='location-data'),
    path('localidad/mes/<str:tipo>', LocationMonthDataView.as_view(), name='location-month-data'),
]