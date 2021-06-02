from flask import render_template, request, Blueprint
from bson.objectid import ObjectId
# from finsite.models import User, Post
from .. import pymongo
from myfinance import predict

companies = Blueprint('companies', __name__)


@companies.route('/company/<company_id>', methods=['POST', 'GET'])
def company(company_id):
    company = pymongo.STOCKS_YF_NIFTY500.stocks_data.find_one({"_id": ObjectId(company_id)})

    return render_template('company.html', company=company)


@companies.route('/basic', methods=['POST', 'GET'])
def basic():
    display = request.args.get('display', 20, type=int)
    companies_data = list(pymongo.STOCKS_YF_NIFTY500.stocks_data.find())
    dfs = predict.make_prediction(input_data=list(companies_data), type='basic')
    return render_template('basic_score.html', dfs=dfs.sort_values('Score', ascending=False, axis=1).iloc[:, :display])