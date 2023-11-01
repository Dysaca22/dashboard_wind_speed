from google.oauth2 import service_account
from google.cloud import bigquery
from django.conf import settings
import unicodedata
import os

from .models import Wind, GeneralData, LocationData, LocationMonthData


class Data():
    def __init__(self):
        self.PROJECT = 'wind-project-403600'
        self.DATASET = 'wind_data'

        key = os.path.join(settings.BASE_DIR, 'static/key.json')
        credential = service_account.Credentials.from_service_account_file(key)
        self.client = bigquery.Client(
            credentials = credential,
            project = self.PROJECT
        )

        self.GENERAL_DATA = self.set_general_data()
        self.LOCATION_DATA = self.set_location_data()
        self.LOCATION_MONTH_DATA = self.set_location_month_data()

    def get_ready_data_2023(self, offset, limit):
        sql = """
            SELECT *
            FROM `{}.ready_data_2023`
            ORDER BY date DESC, department, speed
            LIMIT {} OFFSET {}
        """.format(self.DATASET, limit, offset)
        df_data = self.client.query(sql).result().to_dataframe()

        ready_data_2023 = [
            Wind(
                date = data['date'],
                hour = data['hour'],
                minute = data['minute'],
                speed = data['speed'],
                direction = data['direction'],
                department = data['department'],
                state = data['state'],
                region = data['region'],
                latitude = data['latitude'],
                longitude = data['longitude']
            ) for i, data in df_data.iterrows()
        ]
        return ready_data_2023

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
                noRecords = data['no_records']
            ) for i, data in df_data.iterrows()
        ]
        return general_data

    def set_location_data(self):
        sql = """
            SELECT *
            FROM `{}.department_data`
            ORDER BY department
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_data = [
            LocationData(
                location = 'Departamento',
                name = unicodedata.normalize('NFKD', data['department']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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

        sql = """
            SELECT *
            FROM `{}.state_data`
            ORDER BY state
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_data += [
            LocationData(
                location = 'Municipio',
                name = unicodedata.normalize('NFKD', data['state']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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

        sql = """
            SELECT *
            FROM `{}.region_data`
            ORDER BY region
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_data += [
            LocationData(
                location = 'Region',
                name = unicodedata.normalize('NFKD', data['region']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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
        sql = """
            SELECT *
            FROM `{}.department_month_data`
            ORDER BY department, month
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_month_data = [
            LocationMonthData(
                location = 'Departamento',
                name = unicodedata.normalize('NFKD', data['department']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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

        sql = """
            SELECT *
            FROM `{}.state_month_data`
            ORDER BY state
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_month_data += [
            LocationMonthData(
                location = 'Municipio',
                name = unicodedata.normalize('NFKD', data['state']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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

        sql = """
            SELECT *
            FROM `{}.region_month_data`
            ORDER BY region
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        location_month_data += [
            LocationMonthData(
                location = 'Region',
                name = unicodedata.normalize('NFKD', data['region']).encode('ascii', 'ignore').decode('utf-8').capitalize(),
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

DATA = Data()