from scrapy.item import Item, Field
# from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader

from html2text import html2text

def extract_job_id(value):
    return value.split(":")[-1]

def parse_to_html(value):
    return html2text("".join(value))



class JobsItem(Item):
    # define the fields for your item here like:
    # name = .Field()
    job_id = Field(input_processor=MapCompose(extract_job_id), output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    company_name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    location = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    listed = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    job_url = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    company_url = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    extracted_at = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    search_keyword = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    search_country = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())

    description = Field(input_processor=MapCompose(parse_to_html), output_processor=TakeFirst())
    # description = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # description = Field(dddefault="NULL")
    experience_level = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    employment_type = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    job_function = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    industries = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    salary = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
