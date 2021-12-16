# Maximum Average Income growth calculator

This repository contains a python application that calculates the average growth of incomes for a given list of postal codes during the past 5 years, and returns the postal code with the highest growth percentage.

## How to run:
1- Prepare your environment:

    1-1 First, install mysql server on your machine.
    1-2 Install python 3
    
2- Fill the configuration file under 'configurations' folder with the adequate parameters. ( an example of the config file can be found under './configurations/configuration_example.yaml')

3- Install the project dependencies using the following command:
````
$ pip install - r requirements.txt
````

4- export the project to your PYTHONPATH using the following command:
```
$ export PYTHONPATH='absolute path to the project root'

```

5- Run the program using the following command:
````
$ cd '$the project folder'
$ python average_income/__main__.py configurations/configuration_example.yaml 
````

## Issues faced:
- The table names in the Paavo data source do not follow a naming pattern so I had to retrieve first the table name for the year selected;
- The column attributes in the Paavo data source change from a table to another, for eg. the attribute for the Average income of inhabitants for 2021 data is 'hr_ktu' whilst for 2018 it's 'Hr_ktu', to avoid having a wrong json query for the api call, I first retrieve the metadata for the given year then use it to construct the json query.

## Assumptions made:
- For a given year, the table in the Paavo data source contains data only valid for a previous statistical year ( for eg. "Data published in 2021" contains inhabitants disposable monetary income for 2019 ), therefore, in order to have representative data, the year that I stored in the database was the statistical year;
- I calculated the income growth using latest statistical year available in the database, and the fifth statistical year in the database if ordered in descending order.
- Since only latest five years of data are needed for the calculation, all columns containing data of years previous to those latest five years are dropped.

## Choice of Database type:
- The data is structured, hence choosing SQL over NoSQL.
- Postgres is built with extensibility, SQL standards compliance, scalability, and data integrity in mind and includes features like table inheritance and function overloading - sometimes at the expense of speed. In our case, we are not really concerned with respecting the ACID properties and do not need enhanced features. MySQL was then a better choice to guarantee speed.

## Automation
To schedule a task to run the script yearly (eg every 5th of march), we can use Cron jobs as follows:

1- start editing a cron file by using the command bellow:
````
$ crontab -e
````
2- Depending on your editor (usually Vim), edit the file with the following :
````
0 0 5 3 * '$absolute_python_path' '$absolute_project_path'/average_income/__main__.py  '$absolute_project_path'/configurations/configuration_example.yaml $(date +"%Y") > '$output_file_path'
````