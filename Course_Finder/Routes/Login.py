from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from models import Student, select_Student
from forms import LoginForm  

bcrypt = Bcrypt()

def init_login(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = LoginForm()

        if form.validate_on_submit():
            user = select_Student(form.username.data)

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful.','success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check identifier and password', 'danger')

        return render_template('login.html', title='Login', form=form)
