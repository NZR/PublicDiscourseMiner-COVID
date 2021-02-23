from time import sleep

import scrapy
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl nos-article-css -o ./articles/nos.json```
class NuArticleSpider(scrapy.Spider):
    name = "nu-articles"

    # Get start URLs from json files
    start_urls = []
    with open('sitemapURLs/nu-sitemap.json') as json_file:
        URLlist = json.load(json_file)

        for item in URLlist:
            if item["url"][0] == "/":  # Skip external
                start_urls.append('https://www.nu.nl' + item['url'])

    def parse(self, response):
        try:
            text = response.css("div[class*=article-body] div[class*=block-content]").extract()
            text = ' '.join(text)
            text = BeautifulSoup(text, "html.parser").get_text().strip()
        except:
            text = "VIDEO"

        with open("files/article-" + response.request.url.split("/")[4] + ".html", mode="w", encoding="utf-8") as f:
            f.write(response.text)

        sleep(0.7)

        yield {
            'link': response.request.url,
            'date': response.css("meta[name='article:published_time']::attr(content)").extract_first(),
            'full_text': text,
        }
