from time import sleep

import scrapy
from scrapy.http import Request
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl fd-article-css -o ./articles/fd.json```
class FdArticleSpider(scrapy.Spider):
    name = "fd-article-css"

    # Get start URLs from json files
    start_urls = []
    # with open('./sitemapURLs/fdlinks.json') as json_file: #TODO uncomment deze 4 regels zodra er een fdlinks.json bestaat (anders compilet ie de andere spiders ook niet)
    #     URLlist = json.load(json_file)
    #     for item in URLlist:
    #         start_urls.append(item['url'])

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'cookie-naam':'cookie'}) #TODO zet hier cookie

    def parse(self, response):
        date = "null"
        text = response.css(".article-content-wrap").extract() #TODO zet hier de css class die het artikel wrapt, meestal iets als .post
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        for p in response.css(".xt-post-date"): #TODO zet hier de css class met de datum
            if p.css("time::attr(datetime)").extract_first():
                date = p.css("time::attr(datetime)").extract_first()
        sleep(1) #1 seconde pauze tussen elk artikel ophalen
        yield {
            'link': response.request.url,
            'datum': date,
            'full_text': text,
        }
