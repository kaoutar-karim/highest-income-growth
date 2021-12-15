# Average Income growth calculator

This repository contains a python application that calculates the average growth of incomes for a given list of postal codes during the past 5 years, and returns the postal code with the highest growth percentage.

## How to run:
1- Prepare your environment:

    1-1 First, install mysql server on your machine.
    1-2 Install python 3
    
2- Fill the configuration file under 'configurations' folder with the adequate parameters. ( an example of the conufig file can be found under './configurations/configuration_example.yaml')

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
$ python average_income/__main__.py configurations/configuration_example.yaml 
````