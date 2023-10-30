from google.oauth2 import service_account
from google.cloud import bigquery
from django.conf import settings
import os

from .models import Wind


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
DATA = Data()