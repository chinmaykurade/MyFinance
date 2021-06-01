import pandas as pd

df = pd.read_csv('D:\Code\Projects\MyFinance\myfinance\data\ind_nifty500list.csv')

symbols = list(df['Symbol'])

len(symbols)

