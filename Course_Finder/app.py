from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Database connection settings
host="127.0.0.1"
database="Course Finder"
user="postgres"
password="dis"

def get_db_conn():
    return psycopg2.connect(
        host=host, 
        database=database, 
        user=user, 
        password=password
    )

@app.route('/')
def home():
    conn = get_db_conn()
    curs = conn.cursor()
    
    curs.execute("SELECT * course")
    data = curs.fetchall

    print(data)
    
    conn.close()
    
    return render_template('home.html', data=data)
