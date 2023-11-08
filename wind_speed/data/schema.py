from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene import List, Int, String
from graphene import Schema

from .models import Wind, GeneralData, LocationData, LocationMonthData, GeoData
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
    

class GeoDataType(DjangoObjectType):
    class Meta:
        model = GeoData
        fields = '__all__'


class Query(ObjectType):
    allWind = List(WindType)
    generalData = List(GeneralDataType)
    locationData = List(LocationDataType, location=String(), name=String())
    locationMonthData = List(LocationMonthDataType, location=String(), name=String(), month=Int())
    geoData = List(GeoDataType, location=String())
    
    def resolve_allWind(self, info):
        data = DATA.DATA_DATES
        return data

    def resolve_generalData(self, info):
        return DATA.GENERAL_DATA

    def resolve_locationData(self, info, location=None, name=None):
        location_data = DATA.LOCATION_DATA
        if location:
            location_data =  [*filter(lambda d: d.location == location.lower(), location_data)]
        if name:
            location_data =  [*filter(lambda d: name in d.name.lower(), location_data)]
        return location_data

    def resolve_locationMonthData(self, info, location=None, name=None, month=None):
        location_month_data = DATA.LOCATION_MONTH_DATA
        if location:
            location_month_data =  [*filter(lambda d: d.location == location.lower(), location_month_data)]
        if name:
            location_month_data =  [*filter(lambda d: name in d.name.lower(), location_month_data)]
        if month:
            location_month_data =  [*filter(lambda d: d.month == month, location_month_data)]
        return location_month_data

    def resolve_geoData(self, info, location=None):
        geometry_data = DATA.GEOMETRY_DATA
        if location:
            geometry_data =  [*filter(lambda d: d.location == location.lower(), geometry_data)]
        return geometry_data

schema = Schema(query=Query)