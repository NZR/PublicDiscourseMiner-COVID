import json
import time

import scrapy
from bs4 import BeautifulSoup


class StaOpVoorVrijheidSpider(scrapy.Spider):
    name = "staopvoorvrijheid-articles"

    # Remove the first one
    data = json.load(open("sitemapURLs/staopvoorvrijheid-sitemap.json"))

    start_urls = [item["url"] for item in data]

    def parse(self, response):

        text = response.css(".post").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()

        time.sleep(1)

        yield {
            'link': response.request.url,
            'full_text': text,
            'date': response.css("meta[property='article:published_time']::attr(content)").extract_first()
        }
