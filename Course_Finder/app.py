from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from models import select_Student_by_id
import psycopg2

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)

    login_manager = LoginManager()
    login_manager.init_app(app) 
    @login_manager.user_loader
    def load_user(user_id):
        return select_Student_by_id(user_id)


    # gamle Database connection settings
    host="127.0.0.1"
    database="Course Finder"
    user="postgres"
    password="dis"
    port=5432

    # Database connection settings til testing (ulrik)
    # det her er lidt en cringem måde at gøre det på,
    # men jeg tror de originale settings er gemt ovenfor?

    #host="127.0.0.1"
    #database="postgres"
    #user="postgres"
    #password="dis"
    #port=1333

    def get_db_conn():
        return psycopg2.connect(
            host=host, 
            database=database, 
            user=user, 
            password=password,
            port=port,
        )

    # Routes
    from Routes import Home, View_Review, Write_Review, Login

    Home.init_home(app, get_db_conn)
    View_Review.init_View_Review(app, get_db_conn)
    Write_Review.init_Write_Review(app, get_db_conn)
    # Login.init_login(app)


    return app

























