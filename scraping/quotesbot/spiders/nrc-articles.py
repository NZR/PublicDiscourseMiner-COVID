from time import sleep
import re
import scrapy
from scrapy.http import Request
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl nrc-article-css -o ./articles/nrc.json```
class NrcArticleSpider(scrapy.Spider):
    name = "nrc-article-css"

    # Get start URLs from json files
    start_urls = []
    # with open('./sitemapURLs/nrclinks.json') as json_file: #TODO uncomment deze 4 regels  er een brclinks.json bestaat (anders compilet ie de andere spiders ook niet)
    #     URLlist = json.load(json_file)
    #     for item in URLlist:
    #         start_urls.append(item['url'])

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'FDSSO':'86D4B7A8-2E6F-4D3A-BA37-3AD0B07A380C'}) #TODO zet hier cookie

    def parse(self, response):
        text = response.css(".text_3v_J6Y0G").extract() #TODO zet hier container class van het artikel
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        date = response.css("time::attr(datetime)").extract_first() #TODO sanity check of hier een timestamp in staat
        sleep(1)
        if text != "":
            yield {
                'link': response.request.url,
                'datum': date,
                'full_text': text,
            }
