from time import sleep

import scrapy
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl nos-article-css -o ./articles/nos.json```
class NosArticleSpider(scrapy.Spider):
    name = "nos-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/noslinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append('https://nos.nl' + item['url'])

    def parse(self, response):
        text = response.css(".text_3v_J6Y0G").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        date = response.css("time::attr(datetime)").extract_first()
        sleep(1)
        if text != "":
            yield {
                'link': response.request.url,
                'datum': date,
                'full_text': text,
            }
