all_articles=[]
import csv

with open("articles.csv", encoding="utf8") as f:
    reader=csv.reader(f)
    data=list(reader)
    all_articles=data[1:]
        
liked_articles=[]
unliked_articles=[]