from time import sleep

import scrapy
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl dagelijksestandaard-article-css -o ./articles/dagelijksestandaard.json```
class DagelijkseStandaardArticleSpider(scrapy.Spider):
    name = "dagelijksestandaard-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/dagelijksestandaardlinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])
    del start_urls[0:572] # to get all from 573 onwards, which were dropped in first scrape

    def parse(self, response):
        date = "null"
        text = response.css(".article-content-wrap").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        for p in response.css(".xt-post-date"):
            if p.css("time::text").extract_first():
                date = p.css("time::text").extract_first()
        sleep(0.5)
        yield {
            'link': response.request.url,
            'datum': date,
            'full_text': text,
        }
