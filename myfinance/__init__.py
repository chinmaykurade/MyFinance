import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from pymongo import MongoClient


from . import config
from . import logging_config

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_config.get_console_handler())
logger.propagate = False

VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'
with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
pymongo = MongoClient(os.environ.get('MONGO_URI'))
login_manager.login_view = 'users.login'      # Function name of our route
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # pymongo.init_app(app)

    from .users.routes import users
    from .main.routes import main
    from .companies.routes import companies
    from .transactions.routes import transactions
    # from finsite.errors.handlers import errors
    app.register_blueprint(companies)
    app.register_blueprint(transactions)
    app.register_blueprint(main)
    app.register_blueprint(users)
    # app.register_blueprint(errors)

    # Add command to cli commands
    from .commands import create_tables
    app.cli.add_command(create_tables)

    return app
