
# GovernanceofCyber


## Scraping
All the tools to scrape can be found in the directory _/scraping_. Scraping consists of two parts: First, all the URLs of the articles need to be scraped (sitemap), then, following those URLs, the articles themselves are scraped. 

**Scraping basics**
Every spider file starts in the following way (after some imports):
```
class WebsiteXYZSpider(scrapy.Spider):
    name = "websiteXYZ-sitemap"
    start_urls = []
```
The name is used to call the spider. The usage is as follows: Open the terminal in the /scraping directory and execute one of the following commands:

`scrapy list` returns the list of all spiders which can be used. This command will also try to compile all scrapers, so if any spider refers to a file which does not (yet) exist it will not compile. The simplest way to start is just by commenting out all scrapers which return an error (most likely all _-articles.py_ files since they read from a _links.json_ file which does not yet exist because it was not scraped).

`scrapy crawl <spider name> -o ./filename.json` will execute the spider and place its results in the file _filename.json_

Demo usage:

`scrapy crawl nos-sitemap -o ./sitemapURLs/noslinks.json`

The _start_urls_ list at the beginning lists all the URLs the spider will visit and try to scrape. For scraping articles, this will be filled with all the URLs to the articles.

The hardest part is scraping is finding the right _css selector_ on the page. You can find this by pressing F12 to open the Developer Tool in your browser and selecting the article text. The scrapy documentation https://docs.scrapy.org/en/latest/topics/selectors.html lists a few examples and how to find the correct one. In the end it's getting a bit of practice to find the right selector on a page quickly. Once you have found the selector for one article on a certain site, you can usually use it to scrape all articles from that site.


**Scraping the sitemap**

This is demonstrated by the _*-sitemap.py_ files. It is possible that the site you want to scrape has a sitemap.xml, similar to for example "https://www.transitieweb.nl/post-sitemap.xml". These page scan be scraped by the same spider as the _transitieweb-sitemap.py_ one, the only thing you need to change is the URL in _start_urls_. Instead of the regular scrapy.Spider, this uses an XMLFeedSpider, more information about this can be found at https://docs.scrapy.org/en/latest/topics/spiders.html#xmlfeedspider.

It's also a possibility that you want to scrape all the results of a certain search query on a site. This is demonstrated by for example _nos.sitemap.py_. Usually, the results get displayed on multiple pages and you want to scrape the results of all pages. If there is an iterator in the URL (such as the &page=X in the nos.nl one), you can create a for-loop which iterates over all these pages. Another example is the one from _dagelijksestandaard-sitemap.py_, where the page number is in the middle of the URL.
```
    # NOS sitemap scrape demo
    start_urls = []
    for i in range(1, 213):
        start_urls.append('https://nos.nl/zoeken/?q=corona&page=' + str(i))

```
When scraping URLs you most likely want to save the URLs, this is the _a::attr(href)_ selector in CSS. In the NOS scraper you need to iterate all items in the _.search-results__item_ selector, the demo code of which is stated below:

```
    # NOS sitemap scrape demo
    def parse(self, response):
        sleep(0.5)
        for li in response.css(".search-results__item"):
            yield {
                'url': li.css("a::attr(href)").extract_first()
            }
```

It's easiest to save the URLs you scraped in a file. If you yield the results in the format `'url': <extracted url>` and write the output to a .json file it will be easy to read for the next step. 

**Scraping the articles**

Now that we've got the URLs of the articles we want to scrape in a json file, we can append it to the start_urls list via a for-loop:
```    start_urls = []
    with open('./sitemapURLs/XYZlinks.json') as json_file:
        URLlist = json.load(json_file)
        for item in URLlist:
            start_urls.append(item['url'])
```

If you need to log in to visit the article, you can add your session cookie via the following code:
```
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'<cookie_name>': '<cookie_value>'})
```
The next step is to parse all responses:
```
    def parse(self, response):
        text = response.css(".article_wrapper").extract() # Select the right css wrapper and extract it
        text = ''.join(text) # Wrap all texts together in one string
        text = BeautifulSoup(text, "html.parser").get_text().strip() # Strip the string of all html attributes
        date = response.css("time::attr(datetime)").extract_first() # Select the 'datetime' attribute of the 'time' css wrapper (this is usually the same for all articles)
        sleep(1) # If you don't want to overload the website you're scraping, you can make it pause every article for X seconds
        if text != "": # If the text we have scraped is not empty
            yield {
                'link': response.request.url, #save the URL we have scraped
                'datum': date, # save the article date
                'full_text': text, # save the article text
            }
```

It is possible to save more attributes of the webpage, just add it via the same way as _text_ or _date_, and save it within the _yield_ method.
This is also best written to a .json file, where it will create a list of all scraped articles with the given attributes.
>>>>>>> main
