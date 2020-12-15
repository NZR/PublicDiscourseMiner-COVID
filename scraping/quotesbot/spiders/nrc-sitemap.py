from time import sleep
import scrapy
from scrapy import Request

# usage: `scrapy crawl nrc-sitemap-css -o ./sitemapURLs/nrclinks.json`
class NrcSitemapSpider(scrapy.Spider):
    name = "nrc-sitemap-css"
    start_urls = []
    #TODO als er meerdere pagina's zijn met corona-links, voeg die dan toe aan start_urls. Bij de NOS was dit een simpele
    # pagina-count met zoeken op 'corona'
    for i in range(1, 48):
        start_urls.append('https://fd.nl/search?customPeriod.start=2020-04-01&customPeriod.end=2020-12-13&period=custom-period&tags=Coronavirus&page=' + str(i)) #TODO pas links aan

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'FDSSO':'7D9A361A-F855-46E9-8EF6-99B0BD1BA130', "gdpr-dau": "true"}) #TODO zet hier cookie

    def parse(self, response):
        sleep(0.5)
        for article in response.css(".fd-horizontal-card-3"): #TODO zet hier de class waarin de <a href=""> staat
            yield {
                'url': article.css("a::attr(href)").extract_first()
            }