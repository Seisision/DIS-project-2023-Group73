from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user

# Delete a review from the database
def delete_review_db(review_id, get_db_conn):
    conn = get_db_conn()
    curs = conn.cursor()

    # delete the associated studentreview entry
    query = "DELETE FROM StudentReview WHERE review_id = %s"
    curs.execute(query, (review_id,))

    # delete the review entry
    query = "DELETE FROM Review WHERE id = %s"
    curs.execute(query, (review_id,))

    conn.commit()
    curs.close()
    conn.close()

# update a review in the database
def edit_student_review_db(review_id, new_text, new_score, get_db_conn):
    conn = get_db_conn()
    curs = conn.cursor()

    query = "UPDATE Review SET text = %s, score = %s WHERE id = %s"
    curs.execute(query, (new_text, new_score, review_id))

    conn.commit()
    curs.close()
    conn.close()


def init_My_Reviews(app, get_db_conn):
    # This is the code for the My Reviews page
    @app.route('/my_reviews', methods=['GET', 'POST'])
    def my_reviews():
        if request.method == 'POST':
            review_id = request.form['review_id']
            action = request.form['action']

            if action == 'delete':
                delete_review_db(review_id, get_db_conn)
            elif action == 'edit':
                new_text = request.form['new_text']
                new_score = request.form['new_score']
                edit_student_review_db(review_id, new_text, new_score, get_db_conn)

        conn = get_db_conn()
        curs = conn.cursor()
        
        # Retrieve all of the current user's reviews
        query = """
            SELECT Review.id, Review.year, Review.score, Review.text, Course.name 
            FROM Review 
            JOIN StudentReview ON Review.id = StudentReview.review_id 
            JOIN Course ON Review.course_id = Course.id 
            WHERE StudentReview.student_id = %s
        """
        curs.execute(query, (current_user.id,))
        reviews = curs.fetchall() # Each review is a tuple (id, year, score, text, course_name)

        curs.close()
        conn.close()

        return render_template('my_reviews.html', reviews=reviews)
    
    # This is the code for the Edit Review page
    @app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
    def edit_review(review_id):
        # if the request is a POST, then the user has submitted the form
        if request.method == 'POST':
            # update the review in the database
            new_review_text = request.form['review']
            new_review_score = request.form['score']
            edit_student_review_db(review_id, new_review_text, new_review_score, get_db_conn)
            flash('Review updated!', 'success') # todo - this doesn't work change flash category and handle it properly in the template
            return redirect(url_for('my_reviews'))
        else: # else, the user is requesting the page
            # retrieve the review from the database and render
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute("SELECT text, score FROM Review WHERE id = %s", (review_id,))
            review = cur.fetchone()
            print(f"Review text: {review[0]}, Score: {review[1]}")
            cur.close()
            conn.close()
            return render_template('edit_review.html', review=review, review_id=review_id)


    @app.route('/delete_review/<int:review_id>', methods=['POST'])
    def delete_review(review_id):
        delete_review_db(review_id, get_db_conn)
        flash('Review deleted!', 'success')
        return redirect(url_for('my_reviews'))



    
