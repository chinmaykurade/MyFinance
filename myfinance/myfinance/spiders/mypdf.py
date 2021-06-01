import scrapy
from scrapy.loader import ItemLoader
import logging

from ..items import MyPDFItem


# Helper function to get the url from symbol
def get_url(symbol, table=None):
    return "https://ticker.finology.in/company/" + symbol

class MypdfSpider(scrapy.Spider):
    name = 'mypdf'
    allowed_domains = ['ticker.finology.in']

    # Overriding the __init__ method to pass the argument for symbols
    def __init__(self, name=None, symbols=None, **kwargs):
        super().__init__(name, **kwargs)
        self.symbols = symbols

    # Start the first request
    def start_requests(self):
        url = get_url(self.symbols[0])
        current_index = 0
        try:
            yield (scrapy.Request(url=url, callback=self.parse, dont_filter=True,meta={'current_index': current_index},
                                  headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))
        except IndexError:
            print("No valid URLS found!!")

    def parse(self, response):
        item_loader = ItemLoader(item=MyPDFItem(), response=response)
        # file_url = response.xpath("(//ul[@class='reportsli'])[1]/li/a/@href")
        # logging.error(file_url)
        current_index = response.request.meta['current_index']
        item_loader.add_xpath('file_urls', "(//ul[@class='reportsli'])[1]/li/a/@href")
        item_loader.add_xpath('file_names', "(//ul[@class='reportsli'])[1]/li/a/text()")
        item_loader._add_value('name',self.symbols[current_index])
        yield item_loader.load_item()
        current_index += 1
        if current_index < len(self.symbols):
            next_sym = self.symbols[current_index]
            logging.error(next_sym)
            url = get_url(next_sym)
            yield (
                scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'current_index': current_index},
                               headers={
                                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))
