from flask import render_template, request, Blueprint
# from finsite.models import User, Post
from .. import pymongo
from .utils import *

main = Blueprint('main', __name__)

@main.route('/',methods=['POST', 'GET'])
@main.route('/home',methods=['POST', 'GET'])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    # companies = Company.query.order_by(Company.market_cap.desc()).paginate(page=page, per_page=5)
    companies = list(pymongo.STOCKS_YF_NIFTY500.stocks_data.find().skip((page-1)*per_page).limit(per_page))#[(page-1)*5:page*5]
    # print(len(companies))
    # print(dir(pymongo.db.stocks_data))
    n = len(list(pymongo.STOCKS_YF_NIFTY500.stocks_data.find()))
    num_pages = n//per_page + (1 if n % per_page > 0 else 0)
    print(n, num_pages)
    pages_list = get_page_list(page, num_pages)
    print(pages_list)

    return render_template('home.html', companies=companies, page=page, per_page=per_page, pages_list=pages_list)