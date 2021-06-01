'''
This script connects the database hosting articles, it aggregates
them in a certain structue and it downloads them into a .npy file array.
There are two main collections fetched, articles from the fake_sites 
category and from the real_sites category.
'''
from counter import Counter 
from collections import Counter as CollCount
import nltk
import psycopg2
import numpy as np
from tqdm import tqdm
import json

with open("../../db_credentials.json")as f:
    cred = f.read()
    try:
        cred = json.loads(cred)
        print(cred)
    except ValueError:
        print("json file with wrong syntax")
        

def dbconnect(dbname=cred["dbname"],
              user=cred["user"], 
              password=cred["password"],
              host=cred["host"],
              port=cred["port"]):
                        
    conn = psycopg2.connect(f"dbname={dbname} \
                            user={user} \
                            password={password} \
                            host={host} \
                            port={port}")
    cur = conn.cursor()
    return cur

def fetchArticles(site):
    db = dbconnect()
    db.execute("select full_text from artikelen where site = '"+site+"'")
    return db.fetchall()

def download_articles():
    db = dbconnect()
    db.execute("select distinct site from artikelen where nepnieuws =1")
    fake_sites = db.fetchall()
    db.execute("select distinct site from artikelen where nepnieuws =0")
    real_sites = db.fetchall()
    
    articles = []
    for site in fake_sites:
        c = Counter(real=False)
        articles = fetchArticles(site[0])
        for article in articles:
            c.add_article(article[0])
        articles.append(c)

    for site in real_sites:
        c = Counter(real=True)
        articles = fetchArticles(site[0])
        for article in articles:
            c.add_article(article[0])
        articles.append(c)

        np.save('../../data/articles.npy',articles)

if __name__=="__main__":
    download_articles()
