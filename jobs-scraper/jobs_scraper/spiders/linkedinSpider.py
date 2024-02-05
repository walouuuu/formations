import time
from datetime import datetime
from urllib.parse import urlencode
import httpx
from scrapy.exceptions import DropItem
import asyncio
import logging



import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from jobs_scraper.JobsItem import JobsItem
from scrapy.exceptions import DropItem
from fake_useragent import UserAgent

def days_to_seconds(days):
    return f"r{int(days) * 86400}"

class LinkedinSpider(scrapy.Spider):
    name = "linkedinSpider"
    allowed_domains = ["linkedin.com"]
    start_urls = [
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    ]

    url = None
    params = {}

    # for httpx
    user_agent = UserAgent()
    fake_headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }




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




    async def parse(self, response):
        retries = response.meta.get("retries", 0)

        # if response.status in [400, 999, 429]:
        #     if retries > 3:
        #         html_content = await self.fetch(response.url)
        #         if html_content:
        #             jobs = scrapy.Selector(text=html_content)
        #             # job_details = job_details.xpath('//*[@id="main-content"]/section[1]/div/div/section[1]/div')
        #         else:
        #             raise DropItem(f"Skipping item with empty description: {item}")
        #     else:
        #         yield scrapy.Request(url=response.url, callback=self.parse, meta={"params": response.meta["params"], "retries": retries + 1}, dont_filter=True, priority=1)
        
        params = response.meta["params"]
        jobs = response.xpath('//li/div[contains(@class, "base-card")]')
        for job in jobs:
            
            itemLoader = ItemLoader(item=JobsItem(), selector=job)
            itemLoader.add_xpath('job_id', '@data-entity-urn')
            itemLoader.add_xpath('title', 'a/span/text()')
            itemLoader.add_xpath('company_name', 'div/h4/a/text()')
            itemLoader.add_xpath('location', 'div/div/span/text()')
            itemLoader.add_xpath('listed', 'div/div/time/@datetime')
            itemLoader.add_xpath('salary', './/*[contains(@class, "job-search-card__salary-info")]/text()')
            itemLoader.add_xpath('job_url', 'a/@href')
            itemLoader.add_xpath('company_url', 'div/h4/a/@href')
            itemLoader.add_value('extracted_at', datetime.now().isoformat())
            itemLoader.add_value('search_keyword', params["keywords"])
            itemLoader.add_value('search_country', params["location"])

            job_item = itemLoader.load_item()
            yield scrapy.Request(url=job_item["job_url"], callback=self.parse_full_job, meta={'job_item': job_item})


        params["start"] += 25
        if len(jobs) > 0 and params["start"] < 4000:
        # if len(jobs) > 0 and params["start"] <25:
            self.url = self.start_urls[0] + urlencode(params)
            yield scrapy.Request(url=self.url, callback=self.parse, meta={"params": params, "retries": 0})


    async def parse_full_job(self, response):
        # logging.info(f"INFO : parse_full {response.url}")
        job_item = response.meta['job_item']
        html_content = await self.fetch(response.url)

        if html_content:
            job_details = scrapy.Selector(text=html_content)
            job_details = job_details.xpath('//*[@id="main-content"]/section[1]/div/div/section[1]/div')
            item_loader = ItemLoader(item=job_item, selector=job_details)

            item_loader.add_xpath('description', './/*[contains(@class, "show-more-less-html__markup")]')
            item_loader.add_xpath('experience_level', 'ul/li[1]/span/text()')
            item_loader.add_xpath('employment_type', 'ul/li[2]/span/text()')
            item_loader.add_xpath('job_function', 'ul/li[3]/span/text()')
            item_loader.add_xpath('industries', 'ul/li[4]/span/text()')

            yield item_loader.load_item()
        else:
            yield job_item


    async def fetch(self, url, max_retries=3):

        headers = self.fake_headers
        headers["User-Agent"] = self.user_agent.random
        for _ in range(max_retries): 
            try:
                async with httpx.AsyncClient(timeout=10, headers=headers) as client:
                    response = await client.get(url)
                    response.raise_for_status() 
                    logging.info(f"Fetch succeeded with status code {response.status_code}")
                    return response.text

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in [429, 500, 999]:
                    logging.info(f"Retrying due to status code {exc.response.status_code}")
                    await asyncio.sleep(30)
                else:
                    raise DropItem(f"Skipping item due to HTTP error: {url}")

            except Exception as e:
                logging.warning(f"Unexpected error occurred: {e}") 

        logging.warning(f"Failed to fetch after {max_retries} retries: {url}")
        return None


   