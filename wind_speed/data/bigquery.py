from google.oauth2 import service_account
from google.cloud import bigquery
from django.conf import settings
import os, json

from .models import HourSpeed, GeneralData, LocationData, LocationMonthData, GeoData


class Data():
    def __init__(self):
        self.PROJECT = 'wind-project-404023'
        self.DATASET = 'project'

        key = os.path.join(settings.BASE_DIR, 'static/key.json')
        credential = service_account.Credentials.from_service_account_file(key)
        self.client = bigquery.Client(
            credentials = credential,
            project = self.PROJECT
        )

        self.HOUR_SPEED = self.get_hour_speed()
        self.GENERAL_DATA = self.set_general_data()
        self.LOCATION_DATA = self.set_location_data()
        self.LOCATION_MONTH_DATA = self.set_location_month_data()
        self.GEOMETRY_DATA = self.set_geometry_data()

    def get_hour_speed(self):
        sql = """
            SELECT *
            FROM `{}.hour_speed`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        hour_speed = [
            HourSpeed(
                hour = data['hour'],
                avgSpeed = data['avgSpeed'],
                medSpeed = data['medSpeed']
            ) for i, data in df_data.iterrows()
        ]
        return hour_speed

    def set_general_data(self):
        sql = """
            SELECT *
            FROM `{}.general_data`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        general_data = [
            GeneralData(
                noStates = data['no_states'],
                noDepartments = data['no_departments'],
                noRegions = data['no_regions'],
                noStations = data['no_stations'],
                noRecords = data['no_records']
            ) for i, data in df_data.iterrows()
        ]
        return general_data

    def set_location_data(self):
        location_data = []

        for loc in ['department', 'state', 'region']:
            sql = """
                SELECT *
                FROM `{}.{}_info`
                ORDER BY {}
            """.format(self.DATASET, loc, loc)
            df_data = self.client.query(sql).result().to_dataframe()

            location_data += [
                LocationData(
                    location = loc,
                    name = data[loc],
                    avgSpeed = data['avg_speed'],
                    medianSpeed = data['median_speed'],
                    devSpeed = data['dev_speed'],
                    minSpeed = data['min_speed'],
                    maxSpeed = data['max_speed'],
                    avgDirection = data['avg_direction'],
                    medianDirection = data['median_direction'],
                    devDirection = data['dev_direction']
                ) for i, data in df_data.iterrows()
            ]
        return location_data

    def set_location_month_data(self):
        location_month_data = []

        for loc in ['department', 'state', 'region']:
            sql = """
                SELECT *
                FROM `{}.{}_month_info`
                ORDER BY {}, month
            """.format(self.DATASET, loc, loc)
            df_data = self.client.query(sql).result().to_dataframe()

            location_month_data += [
                LocationMonthData(
                    location = loc,
                    name = data[loc],
                    month = data['month'],
                    avgSpeed = data['avg_speed'],
                    medianSpeed = data['median_speed'],
                    devSpeed = data['dev_speed'],
                    minSpeed = data['min_speed'],
                    maxSpeed = data['max_speed'],
                    avgDirection = data['avg_direction'],
                    medianDirection = data['median_direction'],
                    devDirection = data['dev_direction']
                ) for i, data in df_data.iterrows()
            ]
        return location_month_data

    def set_geometry_data(self):
        geometry_data = []
        
        for loc in ['department', 'state', 'region']:
            sql = """
                SELECT *
                FROM `{}.geo_{}s`
            """.format(self.DATASET, loc)
            df_data = self.client.query(sql).result().to_dataframe()
            
            geometry_data += [
                GeoData(
                    location = loc,
                    name = data[loc.upper()],
                    area = data['AREA'] if 'AREA' in data else None,
                    perimeter = data['PERIMETER'] if 'PERIMETER' in data else None,
                    hectares = data['HECTARES'] if 'HECTARES' in data else None,
                    geometry = json.loads(data['GEOMETRY'])
                ) for i, data in df_data.iterrows()
            ]
        return geometry_data

DATA = Data()