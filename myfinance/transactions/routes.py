from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from myfinance import db
from myfinance.transactions.forms import TransactionForm
from myfinance.models.models import Transaction
from flask_login import  current_user, login_required


transactions = Blueprint('transactions', __name__)


@transactions.route('/transactions/new', methods=['GET', 'POST'])
@login_required
def new_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(date=form.date.data,
                                  action=form.action.data,
                                  unit_price=form.unit_price.data,
                                  symbol=form.symbol.data,
                                  transacted_units=form.transacted_units.data,
                                  fees=form.fees.data,
                                  split_ratio=form.split_ratio.data,
                                  user=current_user) #We can also use user_id
        db.session.add(transaction)
        db.session.commit()
        flash("Your Transaction has been added!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_transaction.html', title="New Transaction", form=form)


@transactions.route('/transactions/<int:transaction_id>', methods=['GET', 'POST'])
def show_transaction(transaction_id):
    # posts = Post.query.get(post_id)
    transaction = Transaction.query.get_or_404(transaction_id)
    return render_template('transaction.html', title=transaction.symbol, transaction=transaction)


@transactions.route('/transactions/<int:transaction_id>/update', methods=['GET', 'POST'])
@login_required
def update_transaction(transaction_id):
    # posts = Post.query.get(post_id)
    transaction = Transaction.query.get_or_404(transaction_id)
    form = TransactionForm()
    if transaction.user != current_user:
        abort(403)
    if form.validate_on_submit():
        transaction.date = form.date.data
        transaction.action = form.action.data
        transaction.transacted_units = form.transacted_units.data
        transaction.symbol = form.symbol.data
        transaction.unit_price = form.unit_price.data
        transaction.fees = form.fees.data
        transaction.split_ratio = form.split_ratio.data
        db.session.commit()
        flash('Your transaction has been updated!', 'success')
        return redirect(url_for('transactions.show_transaction', transaction_id=transaction_id))
    elif request.method == "GET":
        form.date.data = transaction.date
        form.action.data = transaction.action
        form.transacted_units.data = transaction.transacted_units
        form.symbol.data = transaction.symbol
        form.unit_price.data = transaction.unit_price
        form.fees.data = transaction.fees
        form.split_ratio.data = transaction.split_ratio

    return render_template('create_transaction.html', title=transaction.symbol, form=form, legend="Update Transaction")


@transactions.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user != current_user:
        abort(403)
    db.session.delete(transaction)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('users.user_transactions', username=transaction.user.username))
