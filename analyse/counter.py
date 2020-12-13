import json
import re
import nltk
from nltk import bigrams
from nltk.tokenize.toktok import ToktokTokenizer
from collections import Counter as CollCount


class Counter:

    def __init__(self, real):
        self.articles =[]
        self.all_text = ""
        self.real = real

    def add_sites(self, sites):
        for site in sites:
            with open('./data/websites/' + site, 'r') as f:
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

    def get_bigrams(self):
        bgs = bigrams(re.split('\.|\n|\s|,', self.all_text))
        fdist = nltk.FreqDist(bgs)
        return fdist

    def get_words(self):
        fdist = nltk.FreqDist(re.split('\.|\n|\s|,', self.all_text))
        return fdist

    def print_bigrams(self):
        # TODO: remove unwanted bigrams
        fdist = self.get_bigrams()
        for k, v in fdist.items():
            if v > 250:
                print(k, v)

    def print_word(self):
        fdist = self.get_words()
        for k, v in fdist.items():
            print(k, v)

    def x_top_words(self, x):
        return CollCount(self.get_words()).most_common(x)

    def x_top_bigrams(self,x):
        return CollCount(self.get_bigrams()).most_common(x)

if __name__ == "__main__":
    pass

