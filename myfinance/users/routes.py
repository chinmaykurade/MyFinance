from flask import Blueprint, render_template,url_for, redirect, flash, request
from myfinance import db, bcrypt
from myfinance.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from myfinance.models.models import User, Transaction
from myfinance.users.utils import save_picture, send_reset_email
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)

@users.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now Log In', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)


@users.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextpage = request.args.get('next')
            flash(f'Welcome {form.email.data}!', 'success')
            return redirect(nextpage) if nextpage else redirect(url_for('main.home'))
        else:
            flash("Login Unsucessful. Please check email and password", 'danger')
    return render_template('login.html', title="Login", form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash("You are successfully logged out", 'info')
    return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account Details updated successfully", 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # POST GET redirect pattern. Hence, we need to redirect here.
    return render_template('profile.html', title="Profile", image_file=image_file, form=form)


@users.route('/users/<string:username>',methods=['POST','GET'])
def user_transactions(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    transactions = Transaction.query.filter_by(user=user).\
        order_by(Transaction.date.desc()).paginate(page=page, per_page=20)
    return render_template('user_transactions.html', transactions=transactions, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("The link has expired or is invalid!", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f'Your password has been reset! You can now Log In', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)