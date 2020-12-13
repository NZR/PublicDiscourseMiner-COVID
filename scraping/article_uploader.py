import json
from tqdm import tqdm
from database.connector import Ingestor


def upload_json(filename, is_fake):
    is_fake_flag = 1 if is_fake else 0
    db = Ingestor()
    print("Uploading ", filename)
    with open('./articles/' + filename) as json_file:
        data = json.load(json_file)
        for article in tqdm(data):
            ls = db.ingest(link=article['link'], full_text=article['full_text'], datum=article['date'], nep_nieuws=is_fake_flag)
    db.close()


# TODO after datetime is fixed
# upload_json("coronanuchterheid.json", True)
# upload_json("dagelijksestandaard.json", True)
# upload_json("oervaccin.json", True)
# upload_json("xandernieuws.json", True)


# upload_json("staopvoorvrijheid-articles.json", True)
# upload_json("stichtingvaccinvrij-articles.json", True)
# upload_json("transitieweb-articles.json", True)
# upload_json("viruswaarheid-articles.json", True)

