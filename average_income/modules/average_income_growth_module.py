from average_income.utilities.mysql_driver import MysqlDriver
import pandas as pd


class AverageIncome:
    def __init__(self, config):
        self.db_driver = MysqlDriver(config=config)
        self.last_five_years = None

    def get_last_five_years_from_db(self):
        columns = self.db_driver.execute_raw_query(
            "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'average_income'"
        )
        columns = [column[3] for column in columns if column[3] != "postal_code"]
        columns.sort(reverse=True)
        self.last_five_years = columns[:5]

    def calculate_metrics(self):
        if not self.last_five_years:
            self.get_last_five_years_from_db()
        latest_year = self.last_five_years[0]
        five_years_before = self.last_five_years[-1]

        df = pd.read_sql(
            sql=f"SELECT postal_code, (`{latest_year}`-`{five_years_before}`)/`{five_years_before}`*100"
            f" AS perc_growth FROM average_income ORDER BY perc_growth DESC LIMIT 1;",
            index_col="postal_code",
            con=self.db_driver.create_db_connection(),
        )

        return {
            "postal_code": df.iloc[0].name,
            "growth_percentage": df.iloc[0].values[0],
        }
