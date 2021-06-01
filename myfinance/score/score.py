# %% Imports
import pandas as pd
from myfinance.score.intrinsic import intrinsic_value
from myfinance.score import basic_score as bs
from myfinance.score import profitability_ratios as pr
from myfinance.score import solvency_liquidity_ratios as slr
from myfinance.score import activity_ratios as ar
from sklearn.base import BaseEstimator, TransformerMixin


#%% Helper functions
def get_all_ratios(company_table, company_info, company_name):
    pr_table = pr.profitability_ratios(company_table, company_info, company_name, replace=False)
    if isinstance(pr_table, type(None)):
        return None
    ar_table = ar.activity_ratios(company_table, company_info, company_name, replace=False)
    if isinstance(ar_table, type(None)):
        return None
    slr_table = slr.solvency_liquidity_ratios(company_table, company_info, company_name, replace=False)
    if isinstance(slr_table, type(None)):
        return None

    cols_to_use = pr_table.columns.difference(ar_table.columns)
    final_table = ar_table.merge(pr_table[cols_to_use], left_index=True, right_index=True, how='outer')

    cols_to_use = slr_table.columns.difference(final_table.columns)
    final_table = final_table.merge(slr_table[cols_to_use], how='outer', left_index=True, right_index=True)

    return final_table


#%% Class definition
class ScoreStocks(BaseEstimator, TransformerMixin):
    def __init__(self, type='basic'):
        self.type = type

    @staticmethod
    def basic_score(X):
        tables = X['tables']
        infos = X['infos']
        df = pd.DataFrame()
        for (company_name, company_info), (_, company_table) in \
                zip(infos.items(), tables.items()):

            final_table = get_all_ratios(company_table, company_info, company_name)
            if isinstance(final_table, type(None)):
                # print(f"Excluded: {company_name}")
                continue

            values = bs.get_ratios(final_table, company_info)

            int_value, growth_rate = intrinsic_value(company_table, company_info)

            ser = pd.Series(values, name=company_name)
            ser['Intrinsic Value'] = int_value
            ser['Intrinsic Value/CMP'] = int_value / company_info['current_price']
            ser['Score'] = bs.get_basic_score(values)
            df = pd.concat([df, ser], axis=1)

        return df

    @staticmethod
    def piotroski_f_score(X):
        tables = X['tables']
        infos = X['infos']
        df = pd.DataFrame()
        all_tables = {}

        for (company_name, company_info), (_, company_table) in \
                zip(infos.items(), tables.items()):

            if 'Long-term debt' not in list(company_table.columns):
                company_table['Long-term debt'] = 0

            if 'Current debt' not in list(company_table.columns):
                company_table['Current debt'] = 0

            final_table = get_all_ratios(company_table, company_info, company_name)
            if isinstance(final_table, type(None)):
                # print(f"Excluded: {company_name}")
                continue

            final_table['Positive ROA'] = final_table['ROA'] / abs(final_table['ROA'])
            final_table['Positive ROA'] = final_table['Positive ROA'].apply(lambda x: 0 if x == -1 else 1)

            final_table['Positive CFO'] = final_table['Net cash provided by operating activities'] /\
                                          abs(final_table['Net cash provided by operating activities'])
            final_table['Positive CFO'] = final_table['Positive CFO'].apply(lambda x: 0 if x == -1 else 1)

            final_table['Higher ROA'] = 1*(final_table['ROA'] > final_table['ROA'].shift(-1))

            final_table['Higher CFO'] = 1*(final_table['Net cash provided by operating activities']/final_table['Total assets'] >
                                           final_table['ROA'])

            final_table['Decreased Leverage'] = 1*(final_table['Long-term debt'] <
                                                   final_table['Long-term debt'].shift(-1))

            final_table['Higher Current Ratio'] = 1 * (final_table['Current Ratio'] >
                                                     final_table['Current Ratio'].shift(-1))

            final_table['Higher GPM'] = 1 * (final_table['GPM'] >
                                                       final_table['GPM'].shift(-1))

            final_table['Higher Total Asset Turnover'] = 1 * (final_table['Total Asset Turnover'] >
                                                              final_table['Total Asset Turnover'].shift(-1))

            # No new shares were issued
            final_table['Lower Diluted average shares'] =  1 * (final_table['Diluted average shares'] <=\
                                                          final_table['Diluted average shares'].shift(-1))

            final_table['Piotroski F-score'] = final_table.iloc[:, -9:].sum(axis=1)

            values = {x: final_table[x].iloc[0] for x in final_table.iloc[:, -10:]}

            ser = pd.Series(values, name=company_name)
            df = pd.concat([df, ser], axis=1)

            all_tables[company_name] = final_table.dropna(how='all', axis=1)
        return df

    @staticmethod
    def greenblatt_magic_rank(X):
        tables = X['tables']
        infos = X['infos']
        df = pd.DataFrame()
        for (company_name, company_info), (_, company_table) in \
                zip(infos.items(), tables.items()):

            company_table = company_table.fillna(0)

            company_table = pr.profitability_ratios(company_table, company_info, company_name)

            if isinstance(company_table, type(None)):
                continue

            values = {
                'ev': company_table['EV'].iloc[0],
                'ebit': company_table['EBIT'].iloc[0],
                'nopat': company_table['NOPAT'].iloc[0],
                'invested_capital': company_table['Invested Capital'].iloc[0],
                "earnings_yield": company_table['Earnings Yield'].iloc[0],
                'roic': company_table['ROIC'].iloc[0]
            }

            int_value, growth_rate = intrinsic_value(company_table, company_info)

            ser = pd.Series(values, name=company_name)
            ser['Intrinsic Value'] = int_value
            ser['Growth rate'] = growth_rate
            ser['Intrinsic Value/CMP'] = int_value / company_info['current_price']

            df = pd.concat([df, ser], axis=1)

            df.loc['roic_rank'] = df.loc['roic'].rank()
            df.loc['earnings_yield_rank'] = df.loc['earnings_yield'].rank()
            df.loc['rank_sum'] = df.loc['earnings_yield_rank'] + df.loc['roic_rank']
            df.loc['net_rank'] = df.loc['rank_sum'].rank(ascending=False)

            # print(company_name)
            # print(company_table['EV'])
            # print(company_table['EBIT'])
            # print(company_table['Earnings Yield'])
        return df

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        if self.type == 'greenblatt':
            return ScoreStocks.greenblatt_magic_rank(X)
        elif self.type == 'piotroski':
            return ScoreStocks.piotroski_f_score(X)
        else:
            return ScoreStocks.basic_score(X)


# %% Test cell
if __name__ == "__main__":
    from myfinance.preprocess.preprocess import ExtractTablesAndInfos

    MONGO_URI = "mongodb+srv://chinmay:qwer4321@stocksdata.1ijjw.mongodb.net/test?retryWrites=true&w=majority"

    preprocess_obj = ExtractTablesAndInfos(mongo_uri=MONGO_URI, db='STOCKS_YF', collection_name='stocks_data')

    num_data = 10

    all_cd = preprocess_obj.transform(X=None)

    score_obj = ScoreStocks(type='basic')

    dfs = score_obj.predict(all_cd)

