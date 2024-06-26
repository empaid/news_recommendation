import csv
from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:admin@newsomania.ejz4mic.mongodb.net/?retryWrites=true&w=majority&appName=NewsOMania')
db = client['NewsOMania']
collection = db['news']

with open('news_data_3.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        # Check if the article already exists in the collection
        article = collection.find_one({'title': row['title'], 'description': row['description']})
        if article is None:
            collection.insert_one(row)
            print(f"Inserted: {i} rows")
        else:
            print(f"Skipping duplicate article with title '{row['title']}' and description '{row['description']}'")
        
