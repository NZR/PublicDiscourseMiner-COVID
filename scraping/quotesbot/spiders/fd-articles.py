from time import sleep
import re
import scrapy
from scrapy.http import Request
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl fd-article-css -o ./articles/fd.json```
class FdArticleSpider(scrapy.Spider):
    name = "fd-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/fdlinks.json') as json_file: #TODO uncomment deze 4 regels zodra er een fdlinks.json bestaat (anders compilet ie de andere spiders ook niet)
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'FDSSO':'86D4B7A8-2E6F-4D3A-BA37-3AD0B07A380C'}) #TODO zet hier cookie

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
