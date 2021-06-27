from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    action = StringField('Action', validators=[DataRequired()])
    symbol = StringField('Symbol', validators=[DataRequired()])
    transacted_units = FloatField('Transacted Units', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    fees = FloatField('Fees')
    split_ratio = FloatField('Split Ratio', validators=[DataRequired()])
    submit = SubmitField('Add Transaction')
