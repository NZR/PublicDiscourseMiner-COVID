import json
import re
import nltk
from nltk import bigrams
from nltk.tokenize.toktok import ToktokTokenizer

class Counter:

    def __init__(self):
        self.articles =[]
        self.all_text = ""

    def add_sites(self, sites):
        for site in sites:
            with open('../scraping/sitemapURLs/' + site, 'r') as f:
                article = json.load(f)
                for txt in article:
                    txt = txt['full_text']
                    self.add_article(txt)

    def add_article(self, text):
        txt = self.remove_special_characters(text)
        clean_txt = self.remove_stopwords(txt, is_lower_case=True)
        self.articles.append(clean_txt)
        self.all_text+=clean_txt

    def get_articles(self):
        return self.articles

    def remove_special_characters(self, text, remove_digits=False):
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        text = re.sub(pattern, '', text)
        return text.lower()

    # def remove_bigrams(self):
    #     with open('data/deleteBigrams', "r") as file:
    #         remove_list = [i for i in file]
    #     return remove_list

    def remove_stopwords(self, text, is_lower_case=False):
        tokenizer = ToktokTokenizer()
        with open('data/dutch', "r") as file:
            stopword_list = [i.strip() for i in file]
        tokens = tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]

        with open('data/deleteOtherWords.txt', "r") as file:
            delete_word_list = [i.strip() for i in file]
        tokens = filtered_tokens
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in delete_word_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in delete_word_list]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def calc_bigrams(self):
        bgs = bigrams(re.split('\.|\n|\s|,', self.all_text))
        fdist = nltk.FreqDist(bgs)
        return fdist

    def count_words(self):
        fdist = nltk.FreqDist(re.split('\.|\n|\s|,', self.all_text))
        return fdist

    def print_bigrams(self):
        # TODO: remove unwanted bigrams
        fdist = self.calc_bigrams()
        for k, v in fdist.items():
            if v > 250:
                print(k, v)

    def print_word(self):
        fdist = self.count_words()
        for k, v in fdist.items():
            print(k, v)


fake = Counter()
fake_sites = ['staopvoorvrijheid-articles.json', 'stichtingvaccinvrij-articles.json', 'transitieweb-articles.json']
fake.add_sites(fake_sites)
print(fake.print_bigrams())
#
# real = Counter()
# real_sites = ['']
# real.add_sites(real_sites)

def calc_difference(fdist1, fdist2):
    diff = list(set(fdist1.keys())-set(fdist2.keys()))
    print(diff)

