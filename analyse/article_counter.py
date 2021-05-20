import psycopg2


def dbconnect():
    conn = psycopg2.connect("dbname=artikelen user=goc password=governance host=database.mvdboon.nl port=15000")
    cur = conn.cursor()
    return cur


db = dbconnect()
db.execute("select count(*) from artikelen where link LIKE '%nrc.nl%';")
number_of_nrc_articles = db.fetchall()
print(number_of_nrc_articles)

db = dbconnect()
db.execute("select count(*) from artikelen where nepnieuws =1")
fake_sites = db.fetchall()
print(fake_sites)

db.execute("select count(*) from artikelen where nepnieuws =0")
real_sites = db.fetchall()
print(real_sites)
