from graphene_django.views import GraphQLView
from django.urls import path, include
from django.contrib import admin

from data.schema import schema
from service.views import GeneralDataView

urlpatterns = [
    path('', GeneralDataView.as_view(), name='home'),
    path("admin/", admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('service/', include(('service.urls', 'service'), namespace='service')),
]