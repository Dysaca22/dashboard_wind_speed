from google.oauth2 import service_account
from google.cloud import bigquery
from django.conf import settings
import os

from .models import Wind, GeneralData, LocationData, LocationMonthData, GeoData


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

        self.GENERAL_DATA = self.set_general_data()
        self.LOCATION_DATA = self.set_location_data()
        self.LOCATION_MONTH_DATA = self.set_location_month_data()
        self.GEOMETRY_DATA = self.set_geometry_data()

    def get_data_2023(self, offset, limit):
        sql = """
            SELECT *
            FROM `{}.data_2023`
            ORDER BY date DESC, department, speed
            LIMIT {} OFFSET {}
        """.format(self.DATASET, limit, offset)
        df_data = self.client.query(sql).result().to_dataframe()

        data_2023 = [
            Wind(
                date = data['date'],
                code = data['code'],
                region = data['region'],
                department = data['department'],
                state = data['state'],
                latitude = data['latitude'],
                longitude = data['longitude'],
                speed = data['speed'],
                direction = data['direction'],
            ) for i, data in df_data.iterrows()
        ]
        return data_2023

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
        
        for loc in ['department', 'region']:
            sql = """
                SELECT * EXCEPT(GEOMETRY), ST_ASGEOJSON(GEOMETRY) AS GEOMETRY
                FROM `{}.geo_{}s`
            """.format(self.DATASET, loc)
            df_data = self.client.query(sql).result().to_dataframe()
            
            geometry_data += [
                GeoData(
                    location = loc,
                    name = data[loc.upper()],
                    area = data['AREA'],
                    perimeter = data['PERIMETER'],
                    hectares = data['HECTARES'],
                    geometry = data['GEOMETRY']
                ) for i, data in df_data.iterrows()
            ]
        return geometry_data

DATA = Data()