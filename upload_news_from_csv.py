import csv
from pymongo import MongoClient

client = MongoClient('mongodb+srv://python:python@newsomania.zzgeqwh.mongodb.net/?retryWrites=true&w=majority')
db = client['NewsOMania']
collection = db['news']

with open('news_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    cnt = 0
    for i, row in enumerate(reader):
        print(f"Inserted: {i} rows")
        collection.insert_one(row)
        cnt+=1
