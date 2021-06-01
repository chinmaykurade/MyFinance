#%% Imports
from pymongo import MongoClient
import pandas as pd
from myfinance.preprocess.utils import columns_mapper, defaults
from sklearn.base import BaseEstimator, TransformerMixin


#%% The Preprocessing class
class ExtractTablesAndInfos(BaseEstimator, TransformerMixin):
    def __init__(self, mongo_uri=None, db=None, collection_name=None):
        self.mongo_uri = mongo_uri
        self.db = db
        self.collection_name = collection_name

    @staticmethod
    def get_preprocessed_tables(X):
        table_names = ['financials', 'balance_sheet', 'cash_flow']
        all_companies_data = {}
        for company in X:
            company_name = company['company_name']
            dfs = {}

            for table_name in table_names:
                table = company[table_name]
                dfs[table_name] = pd.DataFrame(table, index=table['years']).drop(['years'], axis=1)
            all_companies_data[company_name] = dfs

        return all_companies_data

    @staticmethod
    def get_merged_tables(X, dropTTM = False, dropSep = False):
        table_names = ['financials', 'balance_sheet', 'cash_flow']

        all_cds = ExtractTablesAndInfos.get_preprocessed_tables(X)
        all_cds_merged = {}
        df = pd.DataFrame()
        for company_name, dfs in all_cds.items():
            df = dfs[table_names[0]]
            for table_name in table_names[1:]:
                df = pd.concat([df,dfs[table_name]], axis=1, join='outer')
            if dropSep:
                sep_rows = [row for row in df.index if row.lower().startswith('sep')]
                df.drop(sep_rows,inplace=True)
            if dropTTM:
                ttm_rows = [row for row in df.index if row.lower().startswith('ttm')]
                df.drop(ttm_rows, inplace=True)
                index = df.index
                index = pd.to_datetime(index, format="%d/%m/%Y")
                df.set_index(index, inplace=True)
            df.rename(columns=columns_mapper, inplace=True)
            columns = df.columns.tolist()
            for col, value in defaults.items():
                if col not in columns:
                    df[col] = value
            df = df.loc[:, ~df.columns.duplicated()]
            all_cds_merged[company_name] = df
        return all_cds_merged

    @staticmethod
    def get_infos(X):
        info_keys = [ 'market_cap', 'current_price', 'pe_ratio']
        company_infos = {}
        for company in X:
            company_name = company['company_name']
            company_info = {}
            for k in info_keys:
                try:
                    company_info[k] = company[k]
                except KeyError:
                    company_info[k] = None
            company_infos[company_name] = company_info
        return company_infos

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if X is None:
            client = MongoClient(self.mongo_uri)
            database = client[self.db]
            collection = database[self.collection_name]
            X = list(collection.aggregate([]))
        return {
            'tables': self.get_merged_tables(X, dropTTM=True),
            'infos': self.get_infos(X)
        }



#%% Test cell
if __name__ == "__main__":
    MONGO_URI = "mongodb+srv://chinmay:qwer4321@stocksdata.1ijjw.mongodb.net/test?retryWrites=true&w=majority"

    preprocess_obj = ExtractTablesAndInfos(mongo_uri=MONGO_URI, db='STOCKS_YF', collection_name='stocks_data')

    all_cd = preprocess_obj.transform(X=None)

    all_merged_tables = all_cd['tables']

    infos = all_cd['infos']


