from flask import render_template

def init_View_Review(app, get_db_conn):
    # This is the code for the View Review page
    @app.route('/course_reviews/<int:course_id>')
    def course_reviews(course_id):
        conn = get_db_conn()
        curs = conn.cursor()

        # Get course name
        course_query = "SELECT name FROM Course WHERE id = %s"
        curs.execute(course_query, (course_id,))
        course_name = curs.fetchone()[0]

        # Get reviews
        reviews_query = "SELECT Review.year, Review.score, Review.text, Student.name FROM Review JOIN StudentReview ON Review.id = StudentReview.review_id JOIN Student ON StudentReview.student_id = Student.id WHERE Review.course_id = %s"
        curs.execute(reviews_query, (course_id,))
        reviews = curs.fetchall() # Each review is a tuple (year, score, text, student_name)

        return render_template('course_reviews.html', course_name=course_name, reviews=reviews)