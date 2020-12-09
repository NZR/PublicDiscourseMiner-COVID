import scrapy


class CoronaNuchterheidSpider(scrapy.Spider):
    name = "coronanuchterheid-css"
    start_urls = [
        'https://corona-nuchterheid.nl/sitemap/',
    ]

    def parse(self, response):


        for li in response.css(".entry > ul:nth-child(1) > li:nth-child(2) > ul:nth-child(2) > li"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }

        # for quote in response.css("div.quote"):
        #     yield {
        #         'text': quote.css("span.text::text").extract_first(),
        #         'author': quote.css("small.author::text").extract_first(),
        #         'tags': quote.css("div.tags > a.tag::text").extract()
        #     }
        #
        # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))

