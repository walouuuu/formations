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

        for start_url in self.start_urls:
            
            params = {"PageNumber": 1}

            start_url = start_url + "?" 
            encoded_url = start_url + urlencode(params)
            yield scrapy.Request(url=encoded_url, headers=headers callback=self.parse, meta={"start_url": start_url, "params": params, "retries":0})

    def parse(self, response):
        params = response.meta["params"]
        formations = response.xpath('//*[contains(@class, "formations")]')
        for formation in formations:
            ItemLoader = ItemLoader(item=FormationItem, selector=formation)
            itemLoader.add_xpath('title', 'a/span/text()')
            itemLoader.add_xpath('url', 'div/h4/a/text()')
            itemLoader.add_xpath('lite_description', 'div/h4/a/text()')
            itemLoader.add_xpath('price', 'div/h4/a/@href')

            fromation_item = ItemLoader.load_item()
            yield scrapy.Request(url=formation_item['url'], headers=self.fake_headers, callback=self.pars_full_formation, meta={ "params": params })

        pass
        if len(formations) > 0: 
        # if len(jobs) > 0 and params["start"] <25:
            params["PageNumber"] += 1
            self.url = response.meta["start_url"] + urlencode(params)
            yield scrapy.Request(url=self.url, callback=self.parse, meta={"params": params, "retries": 0})


    async def pars_full_formation(self, response):
        pass
        itemLoader.add_xpath('description', 'div/h4/a/text()')
        itemLoader.add_xpath('logo', '/html/body')
        itemLoader.add_xpath('rating', 'div/div/time/@datetime')
        itemLoader.add_xpath('duree', './/*[contains(@class, "job-search-card__salary-info")]/text()')
        itemLoader.add_xpath('formation_type', 'a/@href')
        itemLoader.add_value('diplomante', datetime.now().isoformat())
        itemLoader.add_value('sub_categorie_id', datetime.now().isoformat())
        itemLoader.add_value('categorie_title', datetime.now().isoformat())
        itemLoader.add_value('categroie_url', datetime.now().isoformat())
        itemLoader.add_value('formateur_nom', datetime.now().isoformat())
        itemLoader.add_value('nom_organisme', datetime.now().isoformat())
        itemLoader.add_value('url_organisme', datetime.now().isoformat())