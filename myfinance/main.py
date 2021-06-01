import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myfinance.spiders.yhofin import YhofinSpider
from myfinance.spiders.mypdf import MypdfSpider
from multiprocessing import Process
import pandas as pd
import time
import os


#%% Importing the symbols
# file_path = "D:\Code\Projects\Screeper\screeper\stocks.txt"
#
# with open(file_path, 'r') as f:
#     data = f.read()
#     f.close()
#
# companies = data.split(',')
# companies = [idd.strip()+'.NS' for idd in companies]

df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\ind_nifty100list.csv')

companies = list(df['Symbol'])
companies = [idd.strip()+'.NS' for idd in companies]

#%% Running the bot
# companies = ['IOC.NS', 'GILLETTE.NS', 'HINDUNILVR.NS', 'COLPAL.NS']
# times = []
# consecutive = 5
# for i in range(len(companies)//consecutive):
#     symbols = companies[consecutive*i:consecutive*(1+i)]
#     process = CrawlerProcess(settings=get_project_settings())
#     process.crawl(YhofinSpider, symbols=symbols)
#     tic = time.time()
#     process.start(stop_after_crawl=False)
#     times.append(time.time() - tic)


#%% Function to create a crawler process
def execute_crawling(symbols=None):
    process = CrawlerProcess(get_project_settings())#same way can be done for Crawlrunner
    # dispatcher.connect(set_result, signals.item_scraped)
    process.crawl(YhofinSpider, symbols=symbols)
    process.start()


#%% Running the scraper process on multiple threads
if __name__ == '__main__':
    # consecutive = 5
    # for i in range(len(companies)//consecutive):
    #     symbols = companies[consecutive * i:consecutive * (1 + i)]
    #     p = Process(target=execute_crawling, kwargs={"symbols": symbols})
    #     p.start()
    #     p.join() # this blocks until the process terminates

        df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\MCAP.csv')
        anrs = os.listdir('D:\Code\Projects\MyFinance\myfinance\data\AnnualReports')
        anros = os.listdir('D:\Code\Projects\MyFinance\myfinance\data\AROther')
        companies = list(df['Symbol'])
        for anr in anrs:
            cname = anr.split('.')[0][:-2]
            # print(cname)
            try:
                companies.remove(cname)
            except:
                continue
        for anr in anros:
            cname = anr.split('.')[0][:-2]
            # print(cname)
            try:
                companies.remove(cname)
            except:
                continue

        # print(companies)
        to_remove = []
        for c in companies:
            try:
                if c.find('&') != -1:
                    to_remove.append(c)
            except:
                print(c)
        for t in to_remove:
            companies.remove(t)


        # companies = ['POWERINDIA']
        process = CrawlerProcess(settings=get_project_settings())
        process.crawl(MypdfSpider, symbols=companies)
        tic = time.time()
        process.start(stop_after_crawl=False)
        toc = time.time()

# #%% Getting the pdf files
# df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\ind_nifty100list.csv')
# companies = list(df['Symbol'])
# process = CrawlerProcess(settings=get_project_settings())
# process.crawl(MypdfSpider, symbols=companies[1:2])
# tic = time.time()
# process.start(stop_after_crawl=False)
# toc = time.time()
