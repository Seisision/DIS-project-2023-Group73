from flask import render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_bcrypt import bcrypt
from models import Student, save_student
from flask_login import current_user

def init_register(app, get_db_conn):
    # Register route
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        # If the user is already logged in, redirect them to the home page
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = RegistrationForm()

        # If the form is submitted and valid, create a new student and save them to the database
        if form.validate_on_submit():
            # Hash the password entered by the user
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Create a new Student object and populate its attributes
            new_student = Student(username=form.username.data, password_hash=hashed_password, name=form.name.data)

            # Save the new student to the database
            save_student(new_student, get_db_conn)  # Implement this function to save the student to the database

            flash('Registration successful. You can now log in.', 'success') # todo chamge flash category to something else and display message on register page
            return redirect(url_for('login'))  # Redirect to the login page
        
        return render_template('register.html', title='Register', form=form)

