import time
from datetime import datetime
from urllib.parse import urlencode
import httpx
from bs4 import BeautifulSoup
# from html2text import html2text

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from jobs_scraper.JobsItem import JobsItem

def days_to_seconds(days):
    return f"r{int(days) * 86400}"

class LinkedinSpider(scrapy.Spider):
    name = "linkedinSpider2"
    allowed_domains = ["linkedin.com"]
    start_urls = [
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    ]

    url = None
    params = {}

    def start_requests(self):
        keywords = self.settings.get("KEYWORDS", "").split(",")
        locations = self.settings.get("LOCATIONS", "").split(",")

        for keyword in keywords:
            for location in locations:
                time.sleep(5)
                params = {
                    "keywords": keyword,
                    "location": location,
                    "f_TPR": days_to_seconds(self.settings.get("PAST_DAYS", 1)),
                    "start": 0,
                }


                self.url = self.start_urls[0] + urlencode(params)
                yield scrapy.Request(url=self.url, callback=self.parse, meta={"params": params, "retries":0})


    def parse(self, response):
        if response.status in [400, 999]:
            # raise CloseSpider("Scrape finish")
            return
        
        params = response.meta["params"]
        jobs = response.xpath('//li/div[contains(@class, "base-card")]')
        for job in jobs:
            
            itemLoader = ItemLoader(item=JobsItem(), selector=job)
            itemLoader.add_xpath('job_id', '@data-entity-urn')
            itemLoader.add_xpath('title', 'a/span/text()')
            itemLoader.add_xpath('company_name', 'div/h4/a/text()')
            itemLoader.add_xpath('location', 'div/div/span/text()')
            itemLoader.add_xpath('listed', 'div/div/time/@datetime')
            itemLoader.add_xpath('salary', './/*[contains(@class, "job-search-card__salary-info")]')
            itemLoader.add_xpath('job_url', 'a/@href')
            itemLoader.add_xpath('company_url', 'div/h4/a/@href')
            itemLoader.add_value('extracted_at', datetime.now().isoformat())
            itemLoader.add_value('search_keyword', params["keywords"])
            itemLoader.add_value('search_country', params["location"])

            job_item = itemLoader.load_item()
            # job_url = f"https://www.linkedin.com/jobs/view/{job_item["job_id"]}"
            job_url = job_item["job_url"]
            yield response.follow(job_url, self.parse_full_job, meta={'job_item': job_item})

        params["start"] += 25
        if len(jobs) > 0 and params["start"] < 300:
        # if len(jobs) > 0 and params["start"] <25:
        # if len(jobs) > 0 and params["start"] < 50:
            self.url = self.start_urls[0] + urlencode(params)
            yield scrapy.Request(url=self.url, callback=self.parse, meta={"params": params, "retries": 0})

    
    async def fetch(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 421 or response.status_code == 999:
                self.logger.warning(f'Received {response.status_code} response for {url}. Handling accordingly...')
                pass
            else:
                return response.text

    # async def parse_full_job_async(self, response):
    async def parse_full_job(self, response):
        job_item = response.meta['job_item']
        job_url = response.url

        html_content = await self.fetch(job_url)



        # job_details = response.xpath('//*[@id="main-content"]/section[1]/div/div/section[1]/div')
        # itemLoader = ItemLoader(item=job_item, selector=job_details)
        if html_content:
            job_details = scrapy.Selector(text=html_content)
            job_details = job_details.xpath('//*[@id="main-content"]/section[1]/div/div/section[1]/div')
            item_loader = ItemLoader(item=job_item, selector=job_details)

            item_loader.add_xpath('description', './/*[contains(@class, "show-more-less-html__markup")]')
            # item_loader.add_xpath('description', './/*[contains(@class, "show-more-less-html__markup")]/text()')
            item_loader.add_xpath('experience_level', 'ul/li[1]/span/text()')
            item_loader.add_xpath('employment_type', 'ul/li[2]/span/text()')
            item_loader.add_xpath('job_function', 'ul/li[3]/span/text()')
            item_loader.add_xpath('industries', 'ul/li[4]/span/text()')
            # //*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span

            yield item_loader.load_item()