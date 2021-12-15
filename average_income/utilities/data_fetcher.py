import json
import re

import requests

import constants as const


class DataFetcher():

    def __init__(self, year:int, postal_codes_list:[str]):
        self.year = year
        self.list_of_postal_codes = postal_codes_list
        self.table_name = None
        self.postal_number_code = None
        self.measures_code = None
        self.average_income_column = None
        self.data_year = None
        self.url = None

    def get_table_name(self):
        list_of_tables_url = f"{const.BASE_URL}/{self.year}"
        response = requests.get(list_of_tables_url).json()
        for res in response:
            if const.TABLE_DESC in res['text']:
                self.table_name = res['id']
        return self.table_name

    def generate_url(self):
        table_name = self.table_name or self.get_table_name()
        self.url = f"{const.BASE_URL}/{self.year}/{table_name}"
        return self.url

    def get_metadata(self):
        url = self.url or self.generate_url()
        return requests.get(url).json()

    def get_json_query_attributes(self):
        metadata = self.get_metadata()
        postal_code_dict = metadata['variables'][0]
        measures_dict = metadata['variables'][1]

        self.postal_number_code = postal_code_dict['code']
        self.measures_code = measures_dict['code']

        column_description_mapping_dict = zip(measures_dict['values'], measures_dict['valueTexts'])
        for column, description in column_description_mapping_dict:
            if "Average income" in description:
                self.average_income_column = column
                self.data_year = re.sub('.*(?P<yr>[0-9]{4}).*', '\g<yr>', description)

    def generate_json_query(self):
        self.get_json_query_attributes()
        query = json.dumps(
            dict(
                query=[
                    dict(
                        code=self.postal_number_code,
                        selection=dict(filter="item", values=self.list_of_postal_codes),
                    ),
                    dict(
                        code=self.measures_code,
                        selection=dict(filter="item", values=[self.average_income_column]),
                    )],
                response=dict(format="json-stat2"),
            ))

        return query

    def fetch_data_from_remote(self):
        data = requests.post(
            url=self.url,
            json=json.loads(self.generate_json_query())
        ).json()
        data['data_year'] = self.data_year

        return data