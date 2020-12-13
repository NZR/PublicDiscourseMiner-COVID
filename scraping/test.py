from database.connector import Ingestor

db = Ingestor()
ls = db.ingest(link="http://test", full_text="dafsd f'adsf ' ''' @:", nep_nieuws=0)
db.close()