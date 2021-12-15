import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


class MysqlDriver:
    def __init__(self, config):
        self.config = config
        self.create_database()
        self.create_db_connection()

    def create_database(self):
        try:
            self.db_connection = mysql.connector.connect(
                host=self.config["HOST"],
                user=self.config["USR"],
                passwd=self.config["PWD"],
            )
            cursor = self.db_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['DATABASE']};")
        except:
            raise Exception("Could not initiate database connection")

    def create_db_connection(self):
        db_connection_str = f'mysql+pymysql://{self.config["USR"]}:{self.config["PWD"]}@localhost:3306/{self.config["DATABASE"]}'
        db_connection = create_engine(db_connection_str)
        return db_connection

    def read_table_from_db(
        self, table_name, index_col=None, list_columns: tuple = None
    ):
        try:
            df = pd.read_sql(
                f"SELECT {','.join(list(list_columns)) if list_columns else '*'} FROM {table_name}",
                con=self.create_db_connection(),
                index_col=index_col,
            )
        except:
            df = pd.DataFrame()
        return df

    def write_table_to_db(self, dataframe, table_name, if_exists="replace"):
        dataframe.to_sql(
            f"{table_name}",
            index=False,
            con=self.create_db_connection(),
            if_exists=if_exists,
        )

    def write_dataframe_to_db(self, dataframe, table_name):
        existing_values = self.read_table_from_db(table_name, index_col="postal_code")
        if not existing_values.empty:
            df_to_write = pd.concat([existing_values, dataframe], axis=1)
            if len(list(df_to_write.columns)) > 5:
                df_to_write = df_to_write.loc[:, ~df_to_write.columns.duplicated()]
                df_to_write = df_to_write.reindex(sorted(df_to_write.columns), axis=1)
                df_to_write = df_to_write.iloc[:, -5:]
            self.write_table_to_db(df_to_write.reset_index(), table_name)
        else:
            self.write_table_to_db(dataframe.reset_index(), table_name)

    def execute_raw_query(self, query):
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows
