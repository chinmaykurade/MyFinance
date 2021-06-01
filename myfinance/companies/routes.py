from flask import render_template, request, Blueprint
from bson.objectid import ObjectId
# from finsite.models import User, Post
from .. import pymongo
from ..preprocess.preprocess import StocksPreprocess
from ..score.score import ScoreStocks

companies = Blueprint('companies', __name__)


@companies.route('/company/<company_id>', methods=['POST', 'GET'])
def company(company_id):
    company = pymongo.STOCKS_YF_NIFTY500.stocks_data.find_one({"_id": ObjectId(company_id)})

    return render_template('company.html', company=company)


@companies.route('/basic', methods=['POST', 'GET'])
def basic():
    display = request.args.get('display', 20, type=int)
    companies_data = list(pymongo.STOCKS_YF_NIFTY500.stocks_data.find().limit(10))
    preprocess_obj = StocksPreprocess(data=list(companies_data))
    all_merged_tables = preprocess_obj.get_merged_tables(dropTTM=True)
    all_infos = preprocess_obj.get_infos()
    score_obj = ScoreStocks(all_merged_tables, all_infos)
    dfs = score_obj.basic_score()
    return render_template('basic_score.html', dfs=dfs.sort_values('Score', ascending=False, axis=1).iloc[:, :display])