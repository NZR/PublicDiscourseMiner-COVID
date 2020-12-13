from time import sleep
import scrapy
from scrapy import Request

# usage: `scrapy crawl fd-sitemap-css -o ./sitemapURLs/fdlinks.json`
class FdSitemapSpider(scrapy.Spider):
    name = "fd-sitemap-css"
    start_urls = []
    #TODO als er meerdere pagina's zijn met corona-links, voeg die dan toe aan start_urls. Bij de NOS was dit een simpele
    # pagina-count met zoeken op 'corona'
    for i in range(1, 213):
        start_urls.append('https://nos.nl/zoeken/?q=corona&page=' + str(i)) #TODO pas links aan

        def start_requests(self):
            for url in self.start_urls:
                yield Request(url, cookies={'cookie-naam':'cookie'}) #TODO zet hier cookie

    def parse(self, response):
        sleep(0.5)
        for li in response.css(".search-results__item"):#TODO zoek de container waarin bijv. <a href=""> zit bij elk zoek/paginaresultaat

            yield {
                'url': li.css("a::attr(href)").extract_first() #TODO mogelijk aanpassen als de link niet in een <a href=""> zit
            }