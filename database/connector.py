import psycopg2


def ingest( link, full_text, datum=None, auteur=None, themes=None, triggers=None, bigrams=None, full_without_stop=None):
    """Ingest function. The link and full_text cannot be left empty, other variables can be empty. Escapement of strings is taken care of."""
    prepared = "PREPARE fooplan (date, text, text, text, text, text, text, text) AS INSERT INTO artikelen VALUES($1, $2, $3, $4, $5, $6, $7, $8); EXECUTE fooplan(%s, %s, %s, %s, %s, %s, %s, %s);"
    conn = psycopg2.connect("dbname=artikelen user=goc password=governance host=database.mvdboon.nl port=15000")
    cur = conn.cursor()
    cur.execute(prepared, (datum, auteur, link, themes, triggers, bigrams, full_without_stop, full_text))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    pass
