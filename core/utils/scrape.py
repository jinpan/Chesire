from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(object):
    browser = None
    query_url = None

    username, password = None, None

    def query(self, keyword):
        return 'Unable to search for %s' % keyword

    def login(self):
        pass

    def __init__(self):
        self.browser = webdriver.PhantomJS()
        self.login()


class WikipediaScraper(Scraper):
    query_url = 'http://en.wikipedia.org/wiki/%s'

    def query(self, keyword):
        self.browser.get(self.query_url % keyword)

        html = self.browser.page_source
        soup = BeautifulSoup(html)
        content = soup.find('div', {'id': 'content'})
        return content


class QuoraScraper(Scraper):
    pass

