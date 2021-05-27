'''
This script connects to a database hosting articles, it aggregates
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


def dbconnect(dbname,user, password,host,port):
    conn = psycopg2.connect(f"dbname={dbname} \
                            user={user} \
                            password={password} \
                            host={host} \
                            port={port}")
    cur = conn.cursor()
    return cur

def fetchArticles(site):
    db = dbconnect("artikelen", "goc", "governance","database.mvdboon.nl", "15000")
    db.execute("select full_text from artikelen where site = '"+site+"'")
    return db.fetchall()

def download_articles():
    db = dbconnect("artikelen", "goc", "governance","database.mvdboon.nl", "15000")
    db.execute("select distinct site from artikelen where nepnieuws =1")
    fake_sites = db.fetchall()
    db.execute("select distinct site from artikelen where nepnieuws =0")
    real_sites = db.fetchall()
    
    counters = []
    for site in fake_sites:
        c = Counter(real=False)
        articles = fetchArticles(site[0])
        for article in articles:
            c.add_article(article[0])
        counters.append(c)

    for site in real_sites:
        c = Counter(real=True)
        articles = fetchArticles(site[0])
        for article in articles:
            c.add_article(article[0])
        counters.append(c)

        np.save('output/articles.npy',counters)

if __name__=="__main__":
    download_articles()
