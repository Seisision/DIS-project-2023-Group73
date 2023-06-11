from flask import render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import current_user

def init_Write_Review(app, get_db_conn):
    # This is the code for the Write Review page
    @app.route('/write_review', methods=['GET', 'POST'])
    def Write_Review():
        conn = get_db_conn()
        cur = conn.cursor()

        # Get courses from the database
        cur.execute("SELECT id, name FROM Course;")
        courses = cur.fetchall()

        # if the request is a POST request, then the user is submitting a review
        if request.method == 'POST':
            course_id = request.form['course']
            review_text = request.form['review']
            review_score = request.form['score']
            review_year = datetime.now().year
            
            # Insert into the database
            student_id = current_user.id

            query = """
                SELECT * FROM CompletedCourses
                WHERE student_id = %s AND course_id = %s
            """
            cur.execute(query, (student_id, course_id))

            if cur.rowcount == 0:
                # The student has not completed the course
                cur.close()
                conn.close()
                error_message = 'You have not completed the course you are trying to review. You can add courses to your completed list under "Completed Courses" on the home page.'
                return render_template('Write_Reviews.html', error_message=error_message, courses=courses)
            
            # Check if the user has already reviewed the selected course
            query = """
                SELECT EXISTS (
                    SELECT 1 FROM StudentReview JOIN Review ON StudentReview.review_id = Review.id
                    WHERE StudentReview.student_id = %s AND course_id = %s
                ) AS reviewed;
            """
            cur.execute(query, (student_id, course_id))
            result = cur.fetchone()
            reviewed = result[0] if result else False

            if reviewed:
                cur.close()
                conn.close()
                error_message = 'You have already reviewed this course. Please edit your review or delete it under "My reviews"'
                return render_template('Write_Reviews.html', error_message=error_message, courses=courses)

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
            error_message="Your review has been submitted"
            return render_template('Write_Reviews.html', error_message=error_message, courses=courses)

        
        else: # else the request is a GET request, so the user is just viewing the page
            cur.close()
            conn.close()
            return render_template('Write_Reviews.html', courses=courses) 

