import json
import os
from time import sleep

link = {}
article = {}
scraped = []

with open('./sitemapURLs/fdlinks.json', "r+") as linkfile:
    with open('./articles/fd.json', 'r+') as articlefile:
        link = json.load(linkfile)
        article = json.load(articlefile)
        for row in article:

                for k,v in row.items():
                    if k == 'link':
                        scraped.append(v)

links = link.copy()
for scrape in scraped:
    for row in links:
        for k,v in row.items():
            # print(k,v)
            # sleep(2)
            if k == 'url':
                if scrape == v:
                    # print(f'Al gescraped: {scrape}')
                    links.remove(row)
# print(len(scraped))
# print(len(link))
# print(len(links))
with open('fdlinks-clean.json', 'w+') as file:
    json.dump(links, file, indent=4)

mylist= article.copy()
mylist = list(dict.fromkeys(str(article)))
print(len(mylist))
print(len(article))
