import scrapy

# usage: `scrapy crawl xandernieuws-sitemap-css -o ./sitemapURLs/xandernieuwslinks.json`
class XandernieuwsSpider(scrapy.Spider):
    name = "xandernieuws-sitemap-css"
    start_urls = ['https://www.xandernieuws.net/category/corona/']
    for i in range(2, 22):
        start_urls.append('https://www.xandernieuws.net/category/corona/page/' + str(i))


    def parse(self, response):

        for li in response.css(".post > header:nth-child(1) > h2:nth-child(1) > a"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }
