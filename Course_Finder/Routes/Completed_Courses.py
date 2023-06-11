from flask import render_template, flash, redirect, url_for
from forms import CompletedCourseForm
from models import save_completed_course, get_completed_courses, delete_student_completed_course
from flask_login import current_user

def init_Completed_Courses(app, get_db_conn):
    # handle completed courses route
    @app.route('/completed_courses', methods=['GET', 'POST'])
    def completed_courses():
        conn = get_db_conn()
        cur = conn.cursor()

        # Ensure user is logged in
        if not current_user.is_authenticated:
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('login'))

        form = CompletedCourseForm()

        # Handling form submission to register a completed course
        if form.validate_on_submit():
            print('Form validated')
            course_id = form.course_id.data
            completion_date = form.completion_date.data

            # Insert into CompletedCourses table
            try:
                save_completed_course(current_user.id, course_id, completion_date, get_db_conn)
                flash('Course registered as completed!', 'success') # todo - change to flash category to something else and display in completedcourses template
            except Exception as e:
                flash(f'Error saving completed course: {str(e)}', 'danger') # todo - change to flash category to something else and display in completedcourses template

        # Retrieve the completed courses for the current user
        completed_courses = get_completed_courses(current_user.id, get_db_conn)

        # Retrieve all courses from the database
        cur.execute("SELECT id, name FROM Course;")
        courses = cur.fetchall()

        cur.close()
        conn.close()

        # Render the template
        return render_template('completed_courses.html', form=form, completed_courses=completed_courses, courses=courses)
    
    # Handle deletion of completed courses
    @app.route('/completed_courses/delete/<int:course_id>', methods=['POST'])
    def delete_completed_course(course_id):
        # Ensure user is logged in
        if not current_user.is_authenticated:
            flash('You need to be logged in to access this page.', 'danger') # todo - change to flash category to something else and display in completedcourses template
            return redirect(url_for('login'))

        # Delete the completed course from the database
        try:
            delete_student_completed_course(current_user.id, course_id, get_db_conn)
            flash('Course deleted successfully!', 'success') # todo - change to flash category to something else and display in completedcourses template
        except Exception as e:
            flash(f'Error deleting course: {str(e)}', 'danger') # todo - change to flash category to something else and display in completedcourses template

        return redirect(url_for('completed_courses'))

    return app