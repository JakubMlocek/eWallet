from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from wallet import db, bcrypt
from wallet.database_connector import User, Transaction
from wallet.users.forms import (RegistrationForm, LoginForm, UpdateAccount,
                                   RequestResetForm, ResetPasswordForm)
from wallet.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Just log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', title="Registration", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('expanses.expanses'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('expanses.expanses'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccount()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file=picture_file
        db.session.commit()
        flash('Updated!','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email      
    image_file=url_for('static', filename='/profile_pictures/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('expanses.expanses'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = user.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email with reset instructions has been sent")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('expanses.expanses'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password has been updated! Just log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('reset_token.html', title="Reset Password", form=form)