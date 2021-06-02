import pandas as pd
import os
# from myfinance.scrape import execute_crawling
from myfinance.config import SCRAPE_FILE

#%%
if __name__ == '__main__':
    df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\ind_nifty100list.csv')
    companies = list(df['Symbol'])
    companies = [idd.strip() + '.NS' for idd in companies]

    # scrape.scrape_companies(symbols=companies)
    command = f'python {SCRAPE_FILE}'
    print(SCRAPE_FILE)
    os.system(command)
    # os.system('dir')
    # execute_crawling(symbols=companies[:5])

    # file = open(r'myfinance/scrape.py', 'r').read()
    # exec(file)

