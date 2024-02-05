from typing import Iterable
import scrapy
from scrapy.http import Request
from fake_useragent import UserAgent
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

from FormationScrapy.formationItem import FormationItem

def get_links_from_sitemap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = [a['href'] for tr in soup.find_all('tr')]
    

class MaformationspiderSpider(scrapy.Spider):
    name = "maformationSpider"
    allowed_domains = ["www.maformation.fr"]
    
    # start_urls = ["https://www.maformation.fr/Formation/Recherche?PageNumber=1"]
    # start_urls = "https://www.maformation.fr/sitemap/sitemap-categorie-domaine_1.xml"
    

    user_agent = UserAgent()
    

    def start_requests(self):

        headers = self.fake_headers
        #headers["User-Agent"] = self.user_agent.random
        start_urls = self.settings.get("LINKS", None)
        fake_headers = self.settings.get("FAKE_HEADERS", None)

        for url in self.start_urls:
            
            params = {"PageNumber": 1}

            url = url + urlencode(params)

            # yield scrapy.Request(url=url, headers=headers callback=self.parse, meta={"params": params, "retries":0})

    def parse(self, response):
        formations = response.xpath('//*[contains(@class, "formations")]')
        for formation in formations:
            ItemLoader = ItemLoader(item=FormationItem, selector=formation)
            itemLoader 
        pass


