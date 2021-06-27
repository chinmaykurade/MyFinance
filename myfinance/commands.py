import click
from flask.cli import with_appcontext

from myfinance import db
# from myfinance.models.models import User,Post

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


