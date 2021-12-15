import pandas as pd
from average_income.utilities import DataFetcher

from average_income.utilities.mysql_driver import MysqlDriver

import constants as const

class DataSaver():

    def __init__(self):
        self.mysql_driver = MysqlDriver(database_name=const.DATABASE)
        self.data_json = None

    def get_data_as_json(self, year, list_of_postal_codes):
        data_fetcher = DataFetcher(
            year=year,
            postal_codes_list=list_of_postal_codes
        )
        data_fetcher.generate_url()
        self.data_json = data_fetcher.fetch_data_from_remote()


    def convert_data_to_dataframe(self):
        if not self.data_json:
            raise ValueError("fetch data as json first")

        df = pd.DataFrame(index=const.POSTAL_CODES)
        df.index.name = 'postal_code'
        df[f"{self.data_json['data_year']}"] = self.data_json['value']

        return df

    def push_data_to_db(self, dataframe):
        self.mysql_driver.write_dataframe_to_db(dataframe, table_name='average_income')
