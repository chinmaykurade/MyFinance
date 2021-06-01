# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.selector import Selector
import re


def str2num(s, multiplier=1):
    if not s or s == '-' or s.lower() == 'n/a':
        return None
    s = s.replace('T', '1E9')
    s = s.replace('M', '1E3')
    s = s.replace('B', '1E6')
    s = s.replace(',', '')
    # s = re.sub(r"[^0-9.]", '', s)
    # if s == '':
    #     return None
    # print(s)

    return float(s)*multiplier


def parse_table(response):
    # Convert the string to a selector object
    table = Selector(text=response)

    rows = table.xpath(".//div[starts-with(@class,'D(tbr)')]")

    # To check for multiplier and currency
    multiplier_info = table.xpath(".//*[@id='Col1-1-Financials-Proxy']/section/div[2]/span/span/text()").get()
    multiplier = 1
    if 'usd' in multiplier_info.lower():
        multiplier = 1*72.63

    try:
        year_cols = rows[0].xpath("./div[starts-with(@class,'Ta(c)')]/*/text()").getall()
    except:
        print(len(rows))
        print(rows)

    row_data = {
        'years': year_cols
    }
    for row in rows[1:]:
        row_name = row.xpath("./div[1]/div[1]/span/text()").get()
        row_contents = row.xpath("./div[starts-with(@class,'Ta(c)')]")
        row_items = []
        for row_content in row_contents:
            row_item = row_content.xpath('./*/text()').get()
            if row_item:
                row_items.append(str2num(row_item, multiplier))
            else:
                row_item = row_content.xpath("./text()").get()
                if not row_item:
                    continue
                row_items.append(str2num(row_item, multiplier))
        if len(row_items) > 0:
            row_data[row_name] = row_items
    return row_data


class MyfinanceItem(scrapy.Item):
    balance_sheet = scrapy.Field(
        input_processor=MapCompose(parse_table),
        output_processor=TakeFirst()
    )
    financials = scrapy.Field(
        input_processor=MapCompose(parse_table),
        output_processor=TakeFirst()
    )
    cash_flow = scrapy.Field(
        input_processor=MapCompose(parse_table),
        output_processor=TakeFirst()
    )
    current_price = scrapy.Field(
        input_processor=MapCompose(str2num),
        output_processor=TakeFirst()
    )
    market_cap = scrapy.Field(
        input_processor=MapCompose(str2num),
        output_processor=TakeFirst()
    )
    pe_ratio = scrapy.Field(
        input_processor=MapCompose(str2num),
        output_processor=TakeFirst()
    )
    company_name = scrapy.Field(
        output_processor=TakeFirst()
    )


class MyPDFItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_names = scrapy.Field()
    name = scrapy.Field(
        output_processor=TakeFirst()
    )


