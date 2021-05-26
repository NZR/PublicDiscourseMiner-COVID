import json
import psycopg2
from tqdm import tqdm
from itertools import islice
import csv
import random

from counter import Counter

class dbconnect():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=artikelen user=goc password=governance host=database.mvdboon.nl port=15000")
        self.cur = self.conn.cursor()
    
    def close(self):
        self.cur.close()
        self.conn.close()
        
    
    def query(self,sql,vars, select=False):
        self.sql = sql
        self.cur.execute(self.sql, vars)
        self.conn.commit()
        if select:
            return self.cur.fetchall()

def db_update(stopwords=True, bigrams=True):
    #get rows, per row ID and full text
    db = dbconnect()
    #Get all rows
    cur_all_rows = db.query("SELECT id, full_text, full_without_stop FROM artikelen", (), True)
    for row in tqdm(cur_all_rows):
        id = row[0]
        full = row[1]
        full_without_stop = row[2]
        
        #remove stop words if wanted
        if stopwords:
            counter = Counter(1)
            filtered = counter.remove_stopwords(counter.remove_special_characters(full, True))
            full_without_stop = filtered
            db.query(f"UPDATE artikelen SET full_without_stop = %s WHERE id = %s", (filtered, id))
        
        #Create bigrams if wanted
        if bigrams:
            counter=Counter(1)
            counter.all_text = full_without_stop
            grams = counter.get_bigrams()
            counted_bigrams = {}
            for k,v in grams.items():
                key = (f'{k[0]} {k[1]}')
                counted_bigrams[key] = v
            gram_str = (json.dumps(counted_bigrams))
            db.query(f'UPDATE artikelen SET bigrams = %s WHERE id = %s', (gram_str, id))
    db.close()
        
def count_bigrams(newnieuws=0, freq=True):
    db = dbconnect()
    bigrams = {}
    cur = db.query("SELECT id, bigrams FROM artikelen WHERE nepnieuws = %s", (newnieuws,), True)
    total_count=0
    for row in cur:
        gram = json.loads(row[1])
        for k,v in gram.items():
            if k not in bigrams:
                bigrams[k] = 0
            bigrams[k] += v
            total_count += v
    bigrams = dict(sorted(bigrams.items(), key=lambda item: item[1]))
    if freq:
        for k,v in bigrams.items():
            bigrams[k] = v / total_count
    db.close()
    return bigrams

def iter_sample_fast(iterable, samplesize):
    results = []
    iterator = iter(iterable)
    # Fill in the first samplesize elements:
    for _ in range(samplesize):
        results.append(iterator.next())
    random.shuffle(results)  # Randomize their positions
    for i, v in enumerate(iterator, samplesize):
        r = random.randint(0, i)
        if r < samplesize:
            results[r] = v  # at a decreasing rate, replace random items

    if len(results) < samplesize:
        raise ValueError("Sample larger than population.")
    return results


if __name__ == "__main__":
    # db_update()
    nep = count_bigrams(1)
    echt = count_bigrams(0)
    print(len(echt.keys()))
    nieuw_keys = list(random.sample(list(echt.keys()), 2652))
    temp = {}
    for key in nieuw_keys:
        temp[key] = echt[key]
    echt=temp
    print(len(echt))
    grams = [nep, echt]
    dist = {}
    for gram in grams:
        for k,v in gram.items():
            dist[k] = 0
    for k,v in nep.items():
        dist[k] += v
    for k,v in echt.items():
        dist[k] = dist[k]-v

    res={}
    dist = dict(sorted(dist.items(), key=lambda item: item[1], reverse=True))
    for k,v in (islice(dist.items(), 100)):
        # print(item)
        res[k]=v
    dist = dict(sorted(dist.items(), key=lambda item: item[1], reverse=False))
    for k,v in  (islice(dist.items(), 100)):
        # print(item)
        res[k]=v

    with open('output_subsample.csv', 'w+') as file:
        for k,v in res.items():
            value = str(v).replace('.', ',')
            file.write(f'{k};{value}\n')


