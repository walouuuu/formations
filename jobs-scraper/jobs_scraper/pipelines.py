# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# class JobsScraperPipeline:
#     def process_item(self, item, spider):
#         for field in item.fields:
#             # item.setdefault(field, 'NULL')
#             item.setdefault(field, None)
#         return item

import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter

class JobsScraperPipeline:
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host=self.mysql_host,
                user=self.mysql_user,
                password=self.mysql_password,
                database=self.mysql_db
            )
            self.cursor = self.conn.cursor()
            self.create_table_if_not_exists(spider)
        except Exception as e:
            spider.logger.error(f"Error connecting to MySQL: {e}")
            raise DropItem("Error connecting to MySQL")

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def create_table_if_not_exists(self, spider):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS job_data (
                job_id VARCHAR(255) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                location VARCHAR(255),
                listed VARCHAR(255),
                job_url VARCHAR(255) NOT NULL,
                company_url VARCHAR(255),
                extracted_at VARCHAR(255),
                search_keyword VARCHAR(255),
                search_country VARCHAR(50),
                description TEXT,
                experience_level VARCHAR(255),
                employment_type VARCHAR(255),
                job_function VARCHAR(255),
                industries VARCHAR(255),
                salary VARCHAR(255)
            )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            spider.logger.info("Table 'job_data' created successfully.")
        except Exception as e:
            spider.logger.error(f"Error creating table 'job_data': {e}")
            raise DropItem("Error creating table 'job_data'")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field in item.fields:
            if not adapter.get(field):
                adapter[field] = None

        try:
            # Check if the item already exists in the database
            check_query = "SELECT job_id FROM job_data WHERE job_id = %s and description is not null"
            self.cursor.execute(check_query, (adapter['job_id'],))
            existing_entry = self.cursor.fetchone()

            if existing_entry:
                spider.logger.info(f"Item with job_id {adapter['job_id']} already exists. Skipping insertion.")
            else:
                # Insert the item into the database
                insert_query = """
                    INSERT INTO job_data (job_id, title, company_name, location, listed, job_url, 
                                      company_url, extracted_at, search_keyword, search_country, description, experience_level,
                                      employment_type, job_function, industries, salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    adapter['job_id'],
                    adapter['title'],
                    adapter['company_name'],
                    adapter['location'],
                    adapter['listed'],
                    adapter['job_url'],
                    adapter['company_url'],
                    adapter['extracted_at'],
                    adapter['search_keyword'],
                    adapter['search_country'],
                    adapter['description'],
                    adapter['experience_level'],
                    adapter['employment_type'],
                    adapter['job_function'],
                    adapter['industries'],
                    adapter['salary'],
                )
                self.cursor.execute(insert_query, values)
                self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error processing item in MySQL: {e}")
            raise DropItem("Error processing item in MySQL")

        return item
