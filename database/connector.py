import psycopg2


class Ingestor():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=artikelen user=goc password=governance host=database.mvdboon.nl port=15000")
        self.cur = self.conn.cursor()
        self.prepared = "PREPARE fooplan (date, text, text, text, text, text, text, text, smallint) AS INSERT INTO artikelen (datum, auteur, link, themes, triggers, bigrams, full_without_stop, full_text, nepnieuws) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9);"
        self.cur.execute(self.prepared)
        self.conn.commit()
    
    def ingest(self, link, full_text, nep_nieuws, datum=None, auteur=None, themes=None, triggers=None, bigrams=None, full_without_stop=None):
        """Ingest function. The link and full_text cannot be left empty, other variables can be empty. Escapement of strings is taken care of."""
        self.sql = "EXECUTE fooplan(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(self.sql, (datum, auteur, link, themes, triggers, bigrams, full_without_stop, full_text, int(nep_nieuws)))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    pass
