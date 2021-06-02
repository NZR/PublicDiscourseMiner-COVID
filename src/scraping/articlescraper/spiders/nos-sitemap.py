from time import sleep

import scrapy

# usage: `scrapy crawl nos-sitemap-css -o ./sitemapURLs/noslinks.json`
class NosSitemapSpider(scrapy.Spider):
    name = "nos-sitemap-css"
    start_urls = []
    for i in range(1, 213):
        start_urls.append('https://nos.nl/zoeken/?q=corona&page=' + str(i))


    def parse(self, response):
        sleep(0.5)
        for li in response.css(".search-results__item"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }