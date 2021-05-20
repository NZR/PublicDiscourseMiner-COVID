from time import sleep
import scrapy
from scrapy.http import Request
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl nrc-article-css -o ./articles/nrc.json```
class NrcArticleSpider(scrapy.Spider):
    name = "nrc-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/nrclinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'nrcnl_session_id': 'cookie_value'})

    def parse(self, response):
        text = ""
        for p in response.css(".content > p"):
            text += p.extract()
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        date = response.css("time::attr(datetime)").extract_first() #TODO sanity check of hier een timestamp in staat
        sleep(0.5)
        if text != "":
            yield {
                'link': response.request.url,
                'datum': date,
                'full_text': text,
            }
