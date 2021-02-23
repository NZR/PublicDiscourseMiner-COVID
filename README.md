# GovernanceofCyber


## Scraping
All the tools to scrape can be found in the directory _/scraping_. Scraping consists of two parts: First, all the URLs of the articles need to be scraped (sitemap), then, following those URLs, the articles themselves are scraped. 

**Scraping basics**


-commands

-start_urls

-css selector

**Scraping the sitemap**

This is demonstrated by the _*-sitemap.py_ files. If you're lucky, the site you want to scrape has a sitemap.xml, similar to for example "https://www.transitieweb.nl/post-sitemap.xml". These page scan be scraped by the same spider as the _transitieweb-sitemap.py_ one, the only thing you need to change is the URL in _start_urls_.
It's also a possibility that you want to scrape all the results of a certain search query on a site. This is demonstrated by for example _nos.sitemap.py_. Usually, the results get displayed on multiple pages and you want to scrape the results of all pages. If there is an iterator in the URL (such as the &page=X in the nos.nl one), you can create a for-loop which iterates over all these pages. Another example is the one from _dagelijksestandaard-sitemap.py_, where the page number is in the middle of the URL.
It's easiest to save the URLs you scraped in a file. If you yield the results in the format 'url': <extracted url> and write the output to a .json file it will be easy to read for the next step. 

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
This is also best written to a .json file, where it will create a list of all scraped articles.