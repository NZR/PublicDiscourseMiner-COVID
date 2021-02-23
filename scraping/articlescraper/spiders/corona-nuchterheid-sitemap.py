import scrapy

# usage: `scrapy crawl coronanuchterheid-sitemap-css -o coronanuchterheidlinks{1,2}.json` for Nieuws or Blog (uncomment)
class CoronaNuchterheidSitemapSpider(scrapy.Spider):
    name = "coronanuchterheid-sitemap-css"
    start_urls = [
        'https://corona-nuchterheid.nl/sitemap/',
    ]

    def parse(self, response):

        # get URLs from "Nieuws"
        for li in response.css(".entry > ul:nth-child(1) > li:nth-child(2) > ul:nth-child(2) > li"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }

        # get URLs from "Blog"
        # for li in response.css(".entry > ul:nth-child(1) > li:nth-child(2) > ul:nth-child(1) > li"):
        #     yield {
        #         'url': li.css("a::attr(href)").extract_first()
        #     }


