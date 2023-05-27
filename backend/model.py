import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bson.objectid import ObjectId

import pandas as pd

# Connect to MongoDB
client = MongoClient('mongodb+srv://python:python@newsomania.zzgeqwh.mongodb.net/?retryWrites=true&w=majority')
db = client['NewsOMania']
news_collection = db['news']
user_collection = db['users']

news_cursor = news_collection.find()
news_list = list(news_cursor)
descriptions = [article['description'] for article in news_list]
ids = [str(article['_id']) for article in news_list]

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(descriptions)
item_similarities = cosine_similarity(tfidf_matrix)


user_id = "ff917cb7-f070-45b9-a714-4e547704ee93"
if 'newsIds' in user_collection.find_one({'userId': user_id}):
    watched_news = user['newsIds']
    watched_news_idx = [ids.index(str(item)) for item in watched_news if str(item) in ids]
# Perform recommendations for a specific user
# user_id = 1
# user_item_data = pd.read_csv("user_rating.csv")
# watched_items = user_item_data.loc[user_item_data['user_id'] == user_id, 'news_id']
# watched_news_idx = [ids.index(str(item)) for item in watched_items if str(item) in ids]
item_scores = item_similarities[watched_news_idx,:].sum(axis=0)
recommendations = item_scores.argsort()[::-1][:10]

# Print out the recommended articles
for i, index in enumerate(recommendations):
    print(str(ids[index]))
    article = news_collection.find_one({'_id': ObjectId(str(ids[index]))})
    print(f"{i + 1}. {article['category']}, {article['title']}")
