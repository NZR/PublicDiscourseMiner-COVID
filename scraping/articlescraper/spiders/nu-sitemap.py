import json
from time import sleep

import scrapy

# usage: `scrapy crawl nu-sitemap -o ./sitemapURLs/noslinks.json`
class NuSitemapSpider(scrapy.Spider):
    name = "nu-sitemap"
    start_urls = []
    # for i in range(0, 16, 8):
    # for i in range(0, 5344, 8):
    for i in range(5344, 5352, 8):
        url = "https://www.nu.nl/block/lean_json/articlelist?order_by=updated_at&footer=ajax&section=coronavirus&title=Het+laatste+nieuws+over+het+coronavirus&section_details=%7B%27geolocation%27%3A+None%2C+%27meta_keywords%27%3A+None%2C+%27intro_bgcolor%27%3A+None%2C+%27is_archived%27%3A+False%2C+%27excerpt%27%3A+None%2C+%27radius%27%3A+None%2C+%27ad_zone%27%3A+%7B%27configuration%27%3A+%7B%27section%27%3A+%27coronavirus%27%7D%2C+%27placement%27%3A+%27coronavirus%27%7D%2C+%27logo_media_id%27%3A+None%2C+%27counts%27%3A+%7B%7D%2C+%27top_slug%27%3A+%27algemeen%27%2C+%27meta_description%27%3A+None%2C+%27style%27%3A+%27nu%27%2C+%27label%27%3A+None%2C+%27parent_slug%27%3A+%27algemeen%27%2C+%27type%27%3A+%27default%27%2C+%27hide_logo%27%3A+False%2C+%27titlebar_color%27%3A+None%2C+%27media_id%27%3A+None%2C+%27description%27%3A+None%2C+%27sponsored_by_short%27%3A+None%2C+%27sidebar_position%27%3A+None%2C+%27slug%27%3A+%27coronavirus%27%2C+%27name%27%3A+%27Coronavirus%27%2C+%27titlebar_bgcolor%27%3A+None%2C+%27intro_color%27%3A+None%2C+%27articlehead_color%27%3A+None%2C+%27flags%27%3A+%5B%5D%2C+%27sponsored_by_long%27%3A+None%2C+%27position%27%3A+None%7D&template=thumb&limit=8&hidden=False&position_in_zone=4&block_id=bac1b6fd3ffa48d89a6f027ba4f58c7d&offset="

        start_urls.append(url + str(i))

    print(start_urls)

    # i = 649

    def parse(self, response):
        sleep(1)

        data = json.loads(response.text)

        with open("files/sitemap-" + str(self.i) + ".json", mode="w", encoding="utf-8") as f:
            f.write(response.text)
            self.i += 1

        for article in data["data"]["context"]["articles"]:
            yield {
                'url': article["url"]
            }