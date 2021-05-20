import psycopg2


class Connector():
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=artikelen user=goc password=governance host=database.mvdboon.nl port=15000")
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def select(self, columns, condition=None, limit=None):
        """ columns can be multiple columns: full_text, nepnieuws.
        Condition is optional """
        query = "select " + columns + " from artikelen"
        if condition:
            query += " where " + condition + ";"
        if limit:
            query += " Limit " + limit
        self.cur.execute(query)
        return self.cur.fetchall()


if __name__ == "__main__":
    pass
