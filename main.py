from flask import Flask, jsonify, request
import csv
from storage import all_articles,liked_articles,unliked_articles
from demographic_filtering import output
from contentbasedfiltering import get_Recommendations
all_articles = []

with open('articles.csv',encoding="utf8") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
not_liked_articles = []

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    movie_data = {
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
        "total_events": all_articles[0][15]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output():
        _d ={
        "url": article[0],
        "title": article[1],
        "text": article[2],
        "lang": article[3],
        "total_events": article[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }),200
    
@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output=get_Recommendations(liked_article[4])
        for data in output:
            all_recommended,append(data)
    import itertools
    all_recommended.sort()
    all_recommended=list(all_recommended for all_recommended ,_ in itertools.groupby(all_recommended))
    article_data=[]
    for recommended in all_recommended:    
        _d ={
        "url": recommended[0],
        "title": recommended[1],
        "text": recommended[2],
        "lang": recommended[3],
        "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }),200
    
if __name__ == "__main__":
  app.run()