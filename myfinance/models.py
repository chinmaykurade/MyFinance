# # from . import db, login_manager
# from datetime import datetime
# from flask_login import UserMixin
# from flask import current_app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default_pic.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)
#
#     def get_reset_token(self, expires_sec=1800):
#         s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
#         return s.dumps({'user_id': self.id}).decode('utf-8')
#
#     @staticmethod
#     def verify_reset_token(token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             user_id = s.loads(token)['user_id']
#         except:
#             return None
#         return User.query.get(user_id)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}'"
#
#
# class Company(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_name = db.Column(db.String(200),nullable=False)
#     sector = db.Column(db.String(100))
#     industry = db.Column(db.String(100))
#     about_company = db.Column(db.Text)
#     market_cap = db.Column(db.Float)
#     current_price = db.Column(db.Float)
#     pe = db.Column(db.Float)
#     book_value = db.Column(db.Float)
#     dividend_yield = db.Column(db.Float)
#     roce = db.Column(db.Float)
#     roe = db.Column(db.Float)
#     # quarters
#     # profit_loss
#     # balance_sheet
#     # cash_flow
#     # ratios
#     # shareholding
#     date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     posts = db.relationship('Quarters', backref='company_name', lazy=True)
#
#     def __repr__(self):
#         return f"Company({self.company_name})  Sector({self.sector})"
#
#
# class Quarters(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     cols = db.Column(db.String(30), nullable=False)
#     sales = db.Column(db.Float)
#     yoy_sales_growth = db.Column(db.Float)
#     expenses = db.Column(db.Float)
#     material_cost = db.Column(db.Float)
#     employee_cost = db.Column(db.Float)
#     operating_profit = db.Column(db.Float)
#     opm = db.Column(db.Float)
#     other_income = db.Column(db.Float)
#     interest = db.Column(db.Float)
#     depreciation = db.Column(db.Float)
#     pbt = db.Column(db.Float)
#     tax = db.Column(db.Float)
#     net_profit = db.Column(db.Float)
#     eps = db.Column(db.Float)
#     company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)