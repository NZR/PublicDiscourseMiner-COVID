import json
import time

import scrapy
from bs4 import BeautifulSoup


class TransitieWebSpider(scrapy.Spider):
    name = "transitieweb-articles"

    # Remove first from this file
    data = json.load(open("sitemapURLs/transitieweb-sitemap.json"))

    start_urls = [item["url"] for item in data]

    def parse(self, response):

        text = response.css(".entry").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()

        time.sleep(1)

        yield {
            'link': response.request.url,
            'full_text': text,
            'date': response.css("meta[property='article:published_time']::attr(content)").extract_first()
        }
