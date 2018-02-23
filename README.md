# theThingsApi

## Getting Started

This project can be used to obtain import data from TheThings platform to a mongodb collection.

### First steps

Before runing the plataform, remember to install the requirements in the 'requirements.txt' file

``` pip install -r requirements.txt```

To run the aplication:

```python import_theThings.py <DateStart>```

DateStart: is the date to start the import, in the format dd-mm-yy HH:MM:SS, if you don't specify any date, it will take yesterday as starting date.


To work with the application, fill in the mongo.json and tokens.json files properly.

