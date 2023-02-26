from fastapi import FastAPI
from typing import Union
import os
import csv
from dotenv import dotenv_values
from pymongo import MongoClient
import datetime as dateTime

config = dotenv_values(".env")


app = FastAPI()




@app.get("/todayCategoriesList")
async def read_root():
    list_of_files = os.listdir(
        "/Users/sanatthukral/My Drive/TU Dublin/year 4/FYP API/API-Lambda/data")
    if len(list_of_files) == 0:
        return None
    latest_file_path = max([os.path.join("/Users/sanatthukral/My Drive/TU Dublin/year 4/FYP API/API-Lambda/data", file)
                           for file in list_of_files], key=os.path.getctime)
    with open(latest_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]

    json_data = []
    for row in data:
        new_row = {}
        new_row['trending_date'] = str(row['trending_date'])
        new_row['category_id'] = int(row['category_id'])
        new_row['views'] = int(row['views'])
        new_row['likes'] = int(row['likes'])
        new_row['comment_count'] = int(row['comment_count'])
        new_row['videos'] = int(row['videos'])
        json_data.append(new_row)

    date = latest_file_path.split("_")[1].split(".")[0]

    return {"Category_Data": json_data}
