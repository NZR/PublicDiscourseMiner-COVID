import json
import psycopg2
from tqdm import tqdm

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
        


if __name__ == "__main__":
    db_update()
