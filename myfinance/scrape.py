import scrapy
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from myfinance.myfinance.spiders.yhofin import YhofinSpider
# from myfinance.myfinance.spiders.mypdf import MypdfSpider
from myfinance.spiders.yhofin import YhofinSpider
from myfinance.spiders.mypdf import MypdfSpider
from multiprocessing import Process
import pandas as pd
import time


#%% Function to create a crawler process
def execute_crawling(symbols=None):
    process = CrawlerProcess(get_project_settings())#same way can be done for Crawlrunner
    # dispatcher.connect(set_result, signals.item_scraped)
    process.crawl(YhofinSpider, symbols=symbols)
    process.start()


def scrape_companies(*, symbols):
    consecutive = 5
    for i in range(len(symbols)//consecutive):
        symbols_small = symbols[consecutive * i:consecutive * (1 + i)]
        p = Process(target=execute_crawling, kwargs={"symbols": symbols_small})
        p.start()
        p.join() # this blocks until the process terminates


def scrape_pdfs(*, symbols):
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(MypdfSpider, symbols=symbols)
    tic = time.time()
    process.start(stop_after_crawl=False)
    toc = time.time()


#%% Running the scraper process on multiple threads
if __name__ == '__main__':
    # df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\MCAP.csv')
    # anrs = os.listdir('D:\Code\Projects\MyFinance\myfinance\data\AnnualReports')
    # anros = os.listdir('D:\Code\Projects\MyFinance\myfinance\data\AROther')
    # companies = list(df['Symbol'])
    # for anr in anrs:
    #     cname = anr.split('.')[0][:-2]
    #     # print(cname)
    #     try:
    #         companies.remove(cname)
    #     except:
    #         continue
    # for anr in anros:
    #     cname = anr.split('.')[0][:-2]
    #     # print(cname)
    #     try:
    #         companies.remove(cname)
    #     except:
    #         continue
    #
    # # print(companies)
    # to_remove = []
    # for c in companies:
    #     try:
    #         if c.find('&') != -1:
    #             to_remove.append(c)
    #     except:
    #         print(c)
    # for t in to_remove:
    #     companies.remove(t)


    # scrape_pdfs(companies=companies)

    df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\ind_nifty100list.csv')
    companies = list(df['Symbol'])
    companies = [idd.strip() + '.NS' for idd in companies]

    # scrape_companies(symbols=companies)
    # execute_crawling(symbols=companies[:5])

    consecutive = 5
    for i in range(len(companies) // consecutive):
        symbols_small = companies[consecutive * i:consecutive * (1 + i)]
        p = Process(target=execute_crawling, kwargs={"symbols": symbols_small})
        p.start()
        p.join()  # this blocks until the process terminates


