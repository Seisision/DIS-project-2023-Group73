from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from models import select_Student_by_username
from forms import LoginForm 

# bcrypt for handling password hashing
bcrypt = Bcrypt()

def init_login(app, get_db_conn):
    # Login route
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # If the user is already logged in, redirect them to the home page
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = LoginForm()

        # If the form is submitted and valid, check if the user exists and log them in
        if form.validate_on_submit():
            user = select_Student_by_username(form.username.data, get_db_conn)
            if user is not None:
                if bcrypt.check_password_hash(user.password_hash, form.password.data):
                    login_user(user, remember=form.remember.data)
                    flash('Login successful.','success')  # todo chamge flash category to something else and display message on login page
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('home')) 
            flash('Login Unsuccessful. Please check identifier and password', 'danger') # todo chamge flash category to something else and display message on login page


        return render_template('login.html', title='Login', form=form)
    
# Logout route
def init_logout(app):
    @app.route("/logout", methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))