import pytz

import API.api_calls as api
import pandas as pd
import json
import datetime
import sys
import pymongo
from pymongo import MongoClient


def import_data(token, contractId, start_date=None, end_date=None):
    device_list = api.get_resources(token)
    dataframe = pd.DataFrame()
    for device in device_list:
        #device = device_list[0]
        print("DEVICE {}".format(device))
        dataframe = dataframe.append(api.get_values(token, device, start_date=start_date, end_date=end_date))
        print("_______________________________")

    dataframe["contractId"] = contractId
    return dataframe


def upload_to_mongo(mongo, dataframe):
    mongo_url = "mongodb://{username}:{password}@{host}:{port}"
    client = MongoClient(mongo_url.format(username=mongo['username'], password=mongo['password'],
                                          host=mongo['host'], port=mongo['port']))
    collection = client[mongo['database']][mongo['collection']]
    collection.insert_many(dataframe.to_dict('records'))

if __name__ == "__main__":
    if len(sys.argv) >1:
        start_date = pytz.UTC.localize(datetime.datetime.strptime(sys.argv[1], "%d-%m-%Y %H:%M:%S"))

    else:
        yesterday = datetime.date.today()-datetime.timedelta(1)
        start_date = pytz.UTC.localize(datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0,0,0))
    tokens = json.load(open("tokens.json"))
    mongo = json.load(open("mongo.json"))
    #start_date = pytz.UTC.localize(datetime.datetime.strptime("01-01-2018 00:00:00", "%d-%m-%Y %H:%M:%S"))
    end_date = pytz.UTC.localize(datetime.datetime.utcnow())
    dataframe = pd.DataFrame()
    tokens = tokens["tokens"]
    for contractId, token in tokens.items():
        #token = tokens.values()[0]
        #contractId = tokens.keys()[0]
        dataframe = dataframe.append(import_data(token, contractId, start_date=start_date, end_date=end_date))
    upload_to_mongo(mongo['mongo'], dataframe)