from time import sleep
import re
import scrapy
from scrapy.http import Request
import json


# usage: ```scrapy crawl fd-article-css -o ./articles/fd.json```


class FdArticleSpider(scrapy.Spider):
    name = "fd-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/fdlinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'FDSSO': 'cookie_value'})  # Add cookie for FD here

    def parse(self, response):
        pattern = r'<script type="application\/ld\+json"((.)*)script>'
        res = re.search(pattern, response.text)
        article = (json.loads(res.group(0)[35:-9]))
        yield {
            'link': response.request.url,
            'datum': article['datePublished'],
            'full_text': article['articleBody'],
            'json': json.dumps(article)
        }
        sleep(0.5)
