import constants as const
import pandas as pd
from average_income.utilities import DataSaver
from average_income.modules import AverageIncome


def main():
    # initiate data saver and avg_income_module
    data_saver = DataSaver()
    avg_income_module = AverageIncome()

    # fill the database with data if not done already
    data_df = pd.DataFrame(index=const.POSTAL_CODES)
    data_df.index.name = 'postal_code'
    for year in const.LIST_OF_YEARS:
        data_saver.get_data_as_json(
            year=year,
            list_of_postal_codes=const.POSTAL_CODES
        )
        data_df[str(data_saver.data_json['data_year'])] = data_saver.convert_data_to_dataframe()
    #push data to db
    data_saver.push_data_to_db(data_df)

    # get the postal code with the highest income growth during the last five years
    results = avg_income_module.calculate_metrics()

    # print the results
    print(f"the postal code {results['postal_code']} had the highest income growth with a percentage of "
          f"{results['growth_percentage']} %")


    #
if __name__ == "__main__":
    main()