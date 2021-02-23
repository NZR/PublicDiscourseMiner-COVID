# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider


class TransitieWebSitemapSpider(XMLFeedSpider):
    name = "transitieweb-sitemap"
    start_urls = [
        'https://www.transitieweb.nl/post-sitemap.xml',
    ]

    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    itertag = 'n:loc'
    iterator = 'xml'

    def parse_node(self, response, node):
        # Ugly
        yield {
            'url': node.extract().replace("<loc xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\">", "").replace("</loc>", ""),
        }