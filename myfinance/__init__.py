import os

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_mail import Mail
from pymongo import MongoClient
from .config import Config


# db = SQLAlchemy()
bcrypt = Bcrypt()
# login_manager = LoginManager()
pymongo = MongoClient(os.environ.get('MONGO_URI'))
# login_manager.login_view = 'users.login'      # Function name of our route
# login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # db.init_app(app)
    bcrypt.init_app(app)
    # login_manager.init_app(app)
    mail.init_app(app)
    # pymongo.init_app(app)

    # from finsite.users.routes import users
    # from finsite.posts.routes import posts
    from .main.routes import main
    from .companies.routes import companies
    # from finsite.errors.handlers import errors
    app.register_blueprint(companies)
    # app.register_blueprint(posts)
    app.register_blueprint(main)
    # app.register_blueprint(errors)

    return app
