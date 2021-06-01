#%% Imports
from pymongo import MongoClient
import pandas as pd
from .utils import columns_mapper, defaults


#%% The Preprocessing class
class StocksPreprocess:
    def __init__(self, data=None, mongo_uri=None, db=None, collection_name=None):
        if data is None:
            client = MongoClient(mongo_uri)
            database = client[db]
            collection = database[collection_name]
            self.data = list(collection.aggregate([]))
        else:
            self.data = data

    def get_preprocessed_tables(self):
        table_names = ['financials', 'balance_sheet', 'cash_flow']
        all_companies_data = {}
        for company in self.data:
            company_name = company['company_name']
            dfs = {}

            for table_name in table_names:
                table = company[table_name]
                dfs[table_name] = pd.DataFrame(table, index=table['years']).drop(['years'], axis=1)
            all_companies_data[company_name] = dfs

        return all_companies_data

    def get_merged_tables(self, dropTTM = False, dropSep = False):
        table_names = ['financials', 'balance_sheet', 'cash_flow']

        all_cds = self.get_preprocessed_tables()
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

    def get_infos(self):
        info_keys = [ 'market_cap', 'current_price', 'pe_ratio']
        company_infos = {}
        for company in self.data:
            company_name = company['company_name']
            company_info = {}
            for k in info_keys:
                try:
                    company_info[k] = company[k]
                except KeyError:
                    company_info[k] = None
            company_infos[company_name] = company_info
        return company_infos


#%% Test cell
if __name__ == "__main__":
    MONGO_URI = "mongodb+srv://chinmay:qwer4321@stocksdata.1ijjw.mongodb.net/test?retryWrites=true&w=majority"

    preprocess_obj = StocksPreprocess(mongo_uri=MONGO_URI, db='STOCKS_YF', collection_name='stocks_data')

    all_cd = preprocess_obj.get_preprocessed_tables()

    all_merged_tables = preprocess_obj.get_merged_tables(dropTTM=True)

    infos = preprocess_obj.get_infos()


