from flask import render_template, request
from datetime import datetime

def init_Write_Review(app, get_db_conn):
    
    @app.route('/write_review', methods=['GET', 'POST'])
    def Write_Review():
        conn = get_db_conn()
        curs = conn.cursor()
        
        if request.method == 'POST':
            course_id = request.form['course']
            review_text = request.form['review']
            review_score = request.form['score']
            review_year = datetime.now().year
            
            # Insert into the database
            conn = get_db_conn()
            cur = conn.cursor()
            
            query = "INSERT INTO Review (year, score, text, course_id) VALUES (%s, %s, %s, %s);"
            cur.execute(query, (review_year, review_score, review_text, course_id))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return 'Review submitted!'
        else:
            # Get courses from the database and pass them to the template
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM Course;")
            courses = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('Write_Reviews.html', courses=courses)

