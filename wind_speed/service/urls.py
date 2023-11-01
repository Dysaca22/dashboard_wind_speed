from django.urls import path

from .views import GeneralDataView


urlpatterns = [
    path('general-data', GeneralDataView.as_view(), name='general-data'),
]