import scrapy
import json
from bs4 import BeautifulSoup

#usage: ```scrapy crawl xandernieuws-article-css -o ./articles/xandernieuws.json```
class XandernieuwsArticleSpider(scrapy.Spider):
    name = "xandernieuws-article-css"

    # Get start URLs from json files
    start_urls = []
    with open('./sitemapURLs/xandernieuwslinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])

    def parse(self, response):
        date = "null"
        text = response.css(".entry-content").extract()
        text = ''.join(text)
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        for p in response.css(".entry-date"):
            if p.css("time::text").extract_first():
                date = p.css("time::text").extract_first()
        yield {
            'link': response.request.url,
            'datum': date,
            'full_text': text,
        }
