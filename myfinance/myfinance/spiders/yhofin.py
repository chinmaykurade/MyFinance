import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy.utils.response import open_in_browser
import time

from ..items import MyfinanceItem

# Helper function to get the url from symbol
def get_url(symbol, table=None):
    if table:
        return 'https://in.finance.yahoo.com/quote/' + symbol + '/' + table +'?p=' + symbol
    return 'https://in.finance.yahoo.com/quote/' + symbol + '/?p=' + symbol


class YhofinSpider(scrapy.Spider):
    name = 'yhofin'
    allowed_domains = ['in.finance.yahoo.com']

    # Overriding the __init__ method to pass the argument for symbols
    def __init__(self, name=None, symbols=None, **kwargs):
        super().__init__(name, **kwargs)
        self.symbols = symbols
        self.tables = ['balance-sheet', 'financials', 'cash-flow']

    # Start the first request
    def start_requests(self):
        url = get_url(self.symbols[0])
        try:
            yield (scrapy.Request(url=url, callback=self.parse, dont_filter=False,
                                  meta={'current_index': 0, 'current_table': self.tables[0]},
                                  headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))
        except IndexError:
            print("No valid URLS found!!")

    def parse(self, response):
        item_loader = ItemLoader(item=MyfinanceItem(), response=response)
        ##
        item_loader.add_xpath('current_price', "//*[@id='quote-header-info']/div[3]/div[1]/div/span[1]/text()")
        item_loader.add_xpath('market_cap', "//*[@id='quote-summary']/div[2]/table/tbody/tr[1]/td[2]/span/text()")
        item_loader.add_xpath('company_name', "//*[@id='quote-header-info']/div[2]/div[1]/div[1]/h1/text()")
        item_loader.add_xpath('pe_ratio', "//*[@id='quote-summary']/div[2]/table/tbody/tr[3]/td[2]/span/text()")

        current_index = response.request.meta['current_index']
        current_table = response.request.meta['current_table']

        url = get_url(self.symbols[current_index], current_table)

        yield (scrapy.Request(url=url, callback=self.parse_table, dont_filter=False,
                              meta={'current_index': current_index, 'current_table': current_table, 'item': item_loader.load_item()},
                              headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))

    def parse_table(self, response):
        # time.sleep(3)
        # Get the current symbol index and the current table to get
        current_index = response.request.meta['current_index']
        current_table = response.request.meta['current_table']

        item = response.request.meta['item']

        rows = response.xpath("//div[starts-with(@class,'D(tbr)')]")
        if len(rows) == 0:
            open_in_browser(response)
            # time.sleep(1)
            url = get_url(self.symbols[current_index])
            logging.info(response.request.headers)
            logging.info(url)
            yield (scrapy.Request(url=url, callback=self.parse, dont_filter=False,
                                  meta={'current_index': current_index, 'current_table': self.tables[0]},
                                  headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))
        else:
            item_loader = ItemLoader(item=item, response=response)

            # Pass the current table to the item loader
            item_loader.add_xpath(current_table.replace('-', '_'), "//*[@id='Main']")

            # If it is the last table, return the data
            if current_table == self.tables[-1]:
                yield item_loader.load_item()
            else:
                # Set the next table as current table and go to the url
                current_table = self.tables[self.tables.index(current_table)+1]
                url = get_url(self.symbols[current_index], current_table)

                yield (scrapy.Request(url=url, callback=self.parse_table, dont_filter=False,
                                      meta={'current_index': current_index, 'current_table': current_table, 'item': item_loader.load_item()},
                                      headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))

            # Check whether there are any more symbols to get, and go to their url
            if len(self.symbols) > current_index + 1:
                url = get_url(self.symbols[current_index+1])
                yield (scrapy.Request(url=url, callback=self.parse, dont_filter=False,
                                      meta={'current_index': current_index + 1, 'current_table': self.tables[0]},
                                      headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}))
            else:
                return None
