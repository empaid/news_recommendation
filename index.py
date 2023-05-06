from flask import Flask, session, request
import uuid
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your-secret-key'
client = MongoClient('mongodb+srv://python:python@newsomania.zzgeqwh.mongodb.net/?retryWrites=true&w=majority')
db = client['NewsOMania']
user_collection = db['users']
news_collection = db['news']


@app.route('/')
def index():
    if 'userId' not in session or user_collection.find_one({'userId' : session.get('userId')}) is None:
        session['userId'] = str(uuid.uuid4())
        print('New User, Session Created, ID: ' + session['userId'])
        user_collection.insert_one({'userId': session['userId'], "newsIds": []})
    else:
        print('Previous User, Session Restored, ID: ' + session['userId'])

    userId = session['userId']
    user = user_collection.find_one({'userId': userId})
    news_cursor = news_collection.find()
    news_list = list(news_cursor)
    descriptions = [article['description'] for article in news_list]
    ids = [str(article['_id']) for article in news_list]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    item_similarities = cosine_similarity(tfidf_matrix)
    if 'newsIds' in user:
        watched_news = user['newsIds']
        watched_news_idx = [ids.index(str(item)) for item in watched_news if str(item) in ids]
    else :
        watched_news_idx = []
    

    item_scores = item_similarities[watched_news_idx,:].sum(axis=0)
    recommendations = item_scores.argsort()[::-1][:30]

    response = ""
    for i, index in enumerate(recommendations):
        print(i)
        article = news_collection.find_one({'_id': ObjectId(str(ids[index]))})
        response += f"{i + 1}. {article['category']}, {article['title']}\n"

    return response


@app.route('/watched/<newsId>', methods=['GET'])
def add_watched_news(newsId) :
    if 'userId' not in session or user_collection.find_one({'userId' : session.get('userId')}) is None:
        session['userId'] = str(uuid.uuid4())
        print('New User, Session Created, ID: ' + session['userId'])
        user_collection.insert_one({'userId': userId, "newsIds": []})

    userId = session['userId']
    result = user_collection.update_one({'userId': userId}, {'$push': {'newsIds': newsId}})

    if result.matched_count == 0:
        return 'Error: User not found'

    return f'News {newsId} watched by user {userId}'

if __name__ == '__main__':
    app.run(debug=True)