from flask import Flask, session, request
import uuid
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bson.objectid import ObjectId
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'
client = MongoClient('mongodb+srv://python:python@newsomania.zzgeqwh.mongodb.net/?retryWrites=true&w=majority')
db = client['NewsOMania']
user_collection = db['users']
news_collection = db['news']


def update_news_list():
    while True:
        print("Updated")
        global news_list, ids, item_similarities
        news_cursor = news_collection.find()
        news_list = list(news_cursor)
        descriptions = [article['description'] for article in news_list]
        ids = [str(article['_id']) for article in news_list]

        # Perform content-based filtering
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        item_similarities = cosine_similarity(tfidf_matrix)

        time.sleep(10)

update_thread = threading.Thread(target=update_news_list)
update_thread.start()

def recommend_articles(watched_news_idx, page_num=1, page_size=20):
    item_scores = item_similarities[watched_news_idx,:].sum(axis=0)
    recommendations = item_scores.argsort()[::-1]
    total_results = len(recommendations)
    
    num_pages = (total_results + page_size - 1) // page_size
    if page_num > num_pages:
        return [], total_results
    
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    page_recommendations = recommendations[start_idx:end_idx]

    articles = []
    for i, index in enumerate(page_recommendations):
        article = news_list[index]
        json_article = {
            'id': str(article['_id']),
            'source': article['source'],
            'author': article['author'],
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'urlToImage': article['urlToImage'],
            'publishedAt': article['publishedAt'],
            'content': article['content'],
            'category': article['category'],
            'country': article['country']
        }
        articles.append(json_article)

    return articles, total_results


@app.route('/recommend')
def index():
    if 'userId' not in session or user_collection.find_one({'userId' : session.get('userId')}) is None:
        session['userId'] = str(uuid.uuid4())
        print('New User, Session Created, ID: ' + session['userId'])
        user_collection.insert_one({'userId': session['userId'], "newsIds": []})
    else:
        print('Previous User, Session Restored, ID: ' + session['userId'])

    userId = session['userId']
    user = user_collection.find_one({'userId': userId})

    if 'newsIds' in user:
        watched_news = user['newsIds']
        watched_news_idx = [ids.index(str(item)) for item in watched_news if str(item) in ids]
    else:
        watched_news_idx = []

    # Get page and pageSize parameters from the request
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 20))

    articles, total_results = recommend_articles(watched_news_idx, page, pageSize)
    response = { "status": "ok", "totalResults": total_results, "articles": articles}

    return response


@app.route('/watch/<newsId>', methods=['GET'])
def add_watched_news(newsId):
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
