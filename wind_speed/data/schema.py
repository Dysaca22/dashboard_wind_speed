from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene import List, Int, String
from graphene import Schema

from .models import Wind, GeneralData, LocationData, LocationMonthData
from .bigquery import DATA


class WindType(DjangoObjectType):
    class Meta:
        model = Wind
        fields = '__all__'


class GeneralDataType(DjangoObjectType):
    class Meta:
        model = GeneralData
        fields = '__all__'


class LocationDataType(DjangoObjectType):
    class Meta:
        model = LocationData
        fields = '__all__'


class LocationMonthDataType(DjangoObjectType):
    class Meta:
        model = LocationMonthData
        fields = '__all__'


class Query(ObjectType):
    allWind = List(WindType, offset=Int(), limit=Int())
    generalData = List(GeneralDataType)
    locationData = List(LocationDataType, location=String(), name=String())
    locationMonthData = List(LocationMonthDataType, location=String(), name=String(), month=Int())
    
    def resolve_allWind(self, info, offset=0, limit=1000):
        if limit > 10000:
            limit = 1000
        data = DATA.get_ready_data_2023(offset, limit)[::-1]
        return data

    def resolve_generalData(self, info):
        return DATA.GENERAL_DATA

    def resolve_locationData(self, info, location=None, name=None):
        location_data = DATA.LOCATION_DATA
        if location:
            location_data =  [*filter(lambda d: d.location == location.capitalize(), location_data)]
        if name:
            location_data =  [*filter(lambda d: name in d.name.capitalize(), location_data)]
        return location_data

    def resolve_locationMonthData(self, info, location=None, name=None, month=None):
        location_month_data = DATA.LOCATION_MONTH_DATA
        if location:
            location_month_data =  [*filter(lambda d: d.location == location.capitalize(), location_month_data)]
        if name:
            location_month_data =  [*filter(lambda d: name in d.name.capitalize(), location_month_data)]
        if month:
            location_month_data =  [*filter(lambda d: d.month == month, location_month_data)]
        return location_month_data

schema = Schema(query=Query)