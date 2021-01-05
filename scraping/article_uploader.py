import json
from tqdm import tqdm
from database.ingestor import Ingestor


def upload_json(filename, is_fake):
    is_fake_flag = 1 if is_fake else 0
    db = Ingestor()
    print("Uploading ", filename)
    with open('./articles/' + filename) as json_file:
        data = json.load(json_file)
        for article in tqdm(data):
            ls = db.ingest(link=article['link'], full_text=article['full_text'], datum=article['datum'], nep_nieuws=is_fake_flag)
    db.close()


# upload_json("nrc_v2.json", False)
# upload_json("nos_v2.json", False)
# upload_json("dagelijksestandaard_v2.json", True)
# upload_json("oervaccin_v2.json", True)
# upload_json("xandernieuws_v2.json", True)


# upload_json("staopvoorvrijheid-articles.json", True)
# upload_json("stichtingvaccinvrij-articles.json", True)
# upload_json("transitieweb-articles.json", True)
# upload_json("viruswaarheid-articles.json", True)

