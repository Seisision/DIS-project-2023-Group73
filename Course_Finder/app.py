from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from models import select_Student_by_id
import psycopg2

def create_app():
    # App settings
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)

    # Login settings
    login_manager = LoginManager()
    login_manager.init_app(app) 
    @login_manager.user_loader
    def load_user(user_id):
        return select_Student_by_id(user_id, get_db_conn)
    
    # Database settings (please enter your own database settings)
    host="127.0.0.1"
    database="postgres"
    user="postgres"
    password="dis"
    port=1333

    # Database connection
    def get_db_conn():
        return psycopg2.connect(
            host=host, 
            database=database, 
            user=user, 
            password=password,
            port=port,
        )

    # Routes
    from Routes import Home, View_Review, Write_Review, Login, Register, Completed_Courses, My_Reviews

    Home.init_home(app, get_db_conn)
    View_Review.init_View_Review(app, get_db_conn)
    Write_Review.init_Write_Review(app, get_db_conn)
    Login.init_login(app, get_db_conn)
    Login.init_logout(app)
    Register.init_register(app, get_db_conn)
    Completed_Courses.init_Completed_Courses(app, get_db_conn)
    My_Reviews.init_My_Reviews(app, get_db_conn)

    return app

























