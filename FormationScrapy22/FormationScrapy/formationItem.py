from scrapy.item import Item, Field
# from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader

# from html2text import html2text

def extract_job_id(value):
    return value.split(":")[-1]

# def parse_to_html(value):
#     return html2text("".join(value))



class FormationItem(Item):
    # define the fields for your item here like:
    # name = .Field()
    formation_id = Field(input_processor=MapCompose(extract_job_id), output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    url = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    logo = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    rating = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    duree = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    formation_type = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    diplomante = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())

    lite_description = Field(input_processor=MapCompose(parse_to_html), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(parse_to_html), output_processor=TakeFirst())
    # description = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # description = Field(dddefault="NULL")
    sub_categorie_id = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    categorie_title = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    categorie_url = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    formateur_nom = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    nom_ogranisme = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    url_organisme = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())