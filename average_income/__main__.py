import constants as const
import pandas as pd
import yaml
import os
import sys
from average_income.utilities import DataSaver
from average_income.modules import AverageIncome


def read_configuration_file(file_path):
    with open(file_path) as conf_file:
        config = yaml.load(conf_file)
    return config


def main():
    # read configuration file
    configuration_file = os.path.join(os.getcwd(), sys.argv[1])
    config = read_configuration_file(configuration_file)

    # initiate data saver and avg_income_module
    data_saver = DataSaver(config=config)
    avg_income_module = AverageIncome(config=config)

    # fill the database with data if not done already
    data_df = pd.DataFrame(index=config["POSTAL_CODES"])
    data_df.index.name = "postal_code"
    for year in config["LIST_OF_YEARS"]:
        data_saver.get_data_as_json(
            year=year,
        )
        data_df[
            str(data_saver.data_json["data_year"])
        ] = data_saver.convert_data_to_dataframe()
    # push data to db
    data_saver.push_data_to_db(data_df)

    # get the postal code with the highest income growth during the last five years
    results = avg_income_module.calculate_metrics()

    # print the results
    print(
        f"the postal code {results['postal_code']} had the highest income growth with a percentage of "
        f"{results['growth_percentage']} %"
    )

    #


if __name__ == "__main__":
    main()
