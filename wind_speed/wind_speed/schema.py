from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene import List, Int
from graphene import Schema

from data.models import Wind
from data.bigquery import DATA


class WindType(DjangoObjectType):
    class Meta:
        model = Wind
        fields = ('date', 'hour', 'minute', 'speed', 'direction', 'department', 'state', 'region', 'latitude', 'longitude')


class Query(ObjectType):
    allWind = List(WindType, offset=Int(), limit=Int())
    
    def resolve_allWind(self, info, offset=0, limit=1000):
        if limit > 10000:
            limit = 1000
        data = DATA.get_ready_data_2023(offset, limit)[::-1]
        return data


schema = Schema(query=Query)