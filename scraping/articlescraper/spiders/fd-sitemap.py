from time import sleep
import scrapy
from scrapy import Request

# usage: `scrapy crawl fd-sitemap-css -o ./sitemapURLs/fdlinks.json`
class FdSitemapSpider(scrapy.Spider):
    name = "fd-sitemap-css"
    start_urls = []
    for i in range(1, 48):  # Number of pages with tag "Coronavirus"
        start_urls.append('https://fd.nl/search?customPeriod.start=2020-04-01&customPeriod.end=2020-12-13&period=custom-period&tags=Coronavirus&page=' + str(i))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'FDSSO': 'coockie_value', "gdpr-dau": "true"})  # Add your FD cookie here

    def parse(self, response):
        # print(response.text)
        sleep(0.5)
        for article in response.css(".fd-horizontal-card-3"):
            yield {
                'url': article.css("a::attr(href)").extract_first()
            }
        for article in response.css(".fd-horizontal-card-3 long-read"):
            yield {
                'url': article.css("a::attr(href)").extract_first()
            }