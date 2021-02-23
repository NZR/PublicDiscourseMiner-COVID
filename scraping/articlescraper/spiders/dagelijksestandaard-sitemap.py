import scrapy


# usage: `scrapy crawl dagelijksestandaard-sitemap-css -o ./sitemapURLs/dagelijksestandaardlinks.json`
class DagelijkseStandaardSitemapSpider(scrapy.Spider):
    name = "dagelijksestandaard-sitemap-css"
    start_urls = ['https://www.xandernieuws.net/category/corona/']
    for i in range(1, 24):
        start_urls.append('https://www.dagelijksestandaard.nl/page/' + str(i) + '/?s=corona')

    def parse(self, response):
        for li in response.css(".post > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > h3:nth-child(2)"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }
