from flask import Flask, session, request, redirect
from flask_session import Session
from flask_cors import CORS, cross_origin
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
import json


app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'your-secret-key'
Session(app)
CORS(app, supports_credentials=True, origins=["*"], allow_headers=["Content-Type"])
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
            'source': json.loads(article['source'].replace('\'', '"').replace("None", "null")),
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


# @app.route('/recommend')
def recommend(userId, page=1, pageSize=20):
    # userId = session['userId']
    user = user_collection.find_one({'userId': userId})

    if 'newsIds' in user:
        watched_news = user['newsIds']
        watched_news_idx = [ids.index(str(item)) for item in watched_news if str(item) in ids]
    else:
        watched_news_idx = []

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

@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    if 'userId' not in session or user_collection.find_one({'userId' : session.get('userId')}) is None:
        session['userId'] = str(uuid.uuid4())
        print('New User, Session Created, ID: ' + session['userId'])
        user_collection.insert_one({'userId': session['userId'], "newsIds": []})
    else:
        print('Previous User, Session Restored, ID: ' + session['userId'])

    # Get page and pageSize parameters from the request
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 20))
    country = request.args.get('country', None)
    category = request.args.get('category', None)

    if(category == 'recommend'):
        return recommend(session['userId'], page=page, pageSize=pageSize)
    # Create query based on country and category parameters
    query = {}
    if country:
        query['country'] = country
    if category:
        query['category'] = category

    # Get total count of articles matching the query
    total_results = news_collection.count_documents(query)

    # Calculate total number of pages
    num_pages = (total_results + pageSize - 1) // pageSize

    # Check if page number is valid
    if page < 1 or page > num_pages:
        return {'status': 'ok', 'totalResults': total_results, 'articles': []}

    # Calculate starting and ending index for articles to return
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize

    # Query for articles matching the query and limit by page size and starting index
    articles_cursor = news_collection.aggregate([ {"$match": query}, {"$project": {
      "publishedAt": {
         "$dateFromString": {
            "dateString": '$publishedAt'
         }
      },
      'source': "$source",
      'author': 'author',
    'title': '$title',
    'description': '$description',
    'url': '$url',
    'urlToImage': '$urlToImage',
    'publishedAt': '$publishedAt',
    'content': '$content',
    'category': '$category',
    'country': '$country'
   }
}, { "$sort": { "publishedAt" : -1} }, {"$skip": start_idx}, {"$limit": pageSize} ])
    articles = [article for article in articles_cursor]

    # Convert articles to JSON format
    json_articles = []
    for article in articles:
        json_article = {
            'id': str(article['_id']),
            'source': json.loads(article['source'].replace('\'', '"').replace("None", "null")),
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
        json_articles.append(json_article)

    # Create response dictionary
    response = {'status': 'ok', 'totalResults': total_results, 'articles': json_articles}
    # response['headers'] = {}
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    app.run(debug=True)
