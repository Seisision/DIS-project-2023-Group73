from flask import render_template, request
from datetime import datetime
from flask_login import current_user

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
            
            student_id = current_user.id

            query = """
                SELECT * FROM CompletedCourses
                WHERE student_id = %s AND course_id = %s
            """
            cur.execute(query, (student_id, course_id))

            if cur.rowcount == 0:
                # The student has not completed the course
                return 'You can only review courses you have completed.'

            # Insert the review into the Review table
            query = "INSERT INTO Review (year, score, text, course_id) VALUES (%s, %s, %s, %s) RETURNING id;"
            cur.execute(query, (review_year, review_score, review_text, course_id))
            review_id = cur.fetchone()[0]  # Retrieve the generated review ID

            # Insert the association into the StudentReview table
            query = "INSERT INTO StudentReview (student_id, review_id) VALUES (%s, %s);"
            cur.execute(query, (student_id, review_id))

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

