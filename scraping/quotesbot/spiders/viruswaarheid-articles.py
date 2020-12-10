import json
import time

import scrapy
from bs4 import BeautifulSoup


class VirusWaarheidSpider(scrapy.Spider):
    name = "viruswaarheid-articles"

    data = json.load(open("sitemapURLs/viruswaarheid-sitemap.json"))

    start_urls = [item["url"] for item in data]
    # start_urls = [[item["url"] for item in data][0]]

    def parse(self, response):

        text = response.css(".et_pb_post_content").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()

        time.sleep(1)

        yield {
            'link': response.request.url,
            'full_text': text,
            'date': response.css("meta[property='article:published_time']::attr(content)").extract_first()
        }
