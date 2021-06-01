#%% Importng libraries
import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set()


#%% Functions


def get_price_data(portfolio_list, start=dt.datetime.today() - dt.timedelta(365), end=dt.datetime.today(), interval='1d'):
    # ohlcv_data = {}
    # for ticker in portfolio_list:
    #     ohlcv_data[ticker] = yf.download(ticker, start, end, interval=interval)

    all_tickers = " ".join(portfolio_list)
    ohlcv_data = yf.download(all_tickers, start, end, threads=True, interval=interval)

    return ohlcv_data


def get_returns_matrix(ohlcv_data):
    df_returns = ohlcv_data['Adj Close'].pct_change()
    return df_returns


def get_betas(ohlcv_data, ohlcv_market, portfolio_list=None):


    ohlcv_data['Adj Close', 'market'] = ohlcv_market['Adj Close']
    df_returns = get_returns_matrix(ohlcv_data)
    if portfolio_list is None:
        df_cov = df_returns.cov()
    else:
        df_cov = df_returns[portfolio_list + ['market']].cov()

    var_m = df_cov.loc['market', 'market']

    betas = df_cov.loc['market', :]/var_m

    return betas


def get_individual_expected_return(portfolio_list, ohlcv_data=None, ohlcv_market=None, num_years=5):
    if ohlcv_data is None:
        ohlcv_data = get_price_data(portfolio_list, start=dt.datetime.today() - dt.timedelta(365 * num_years))
    if ohlcv_market is None:
        ohlcv_market = yf.download('^NSEI', start=dt.datetime.today() - dt.timedelta(365 * num_years))

    betas = get_betas(ohlcv_data, ohlcv_market)

    df_returns = get_returns_matrix(ohlcv_data)
    df_cum_returns = (1 + df_returns).cumprod()
    n = len(df_cum_returns) / 252
    CAGR = (df_cum_returns.iloc[-1, :]) ** (1 / n) - 1

    rf = 0.055

    expected_returns_all = rf + betas*(CAGR.loc['market']-rf)

    return expected_returns_all


def get_pairs_noncorr(dfcorr, thresh=0.2):
    pairs = []
    for i,c in enumerate(dfcorr.columns.to_list()):
        for j,d in enumerate(dfcorr.columns.to_list()[:i+1]):
            # print(c,d)
            if dfcorr.loc[c,d] < thresh:
                pairs.append((c,d))
    return pairs

#%%
if __name__ == '__main__':
    num_years = 5
    # path = 'data/portfolio.txt'
    # with open(path, 'r') as f:
    #     data = f.read().split(',')
    #     f.close()
    # portfolio_list = [x.strip() + '.NS' for x in data]

    df500 = pd.read_csv('data/ind_nifty500list.csv')
    symbols = list(df500['Symbol'])
    symbols = [x + '.NS' for x in symbols]
    ohlcv_data = get_price_data(symbols, start=dt.datetime.today() - dt.timedelta(365 * num_years))

    # ohlcv_data = get_data(portfolio_list,start=dt.datetime.today()-dt.timedelta(365*num_years))
    df_returns = get_returns_matrix(ohlcv_data)

    pairs = get_pairs_noncorr(df_returns.corr(), thresh=-0.02)