from flask import render_template, request, session, redirect, url_for
from flask_login import current_user

def init_home(app, get_db_conn):
    # Home route
    @app.route('/', methods=['GET', 'POST'])
    def home():
        conn = get_db_conn()
        curs = conn.cursor()

        # selected_prerequisites is a list of course names that the user has selected as prerequisites defaults to an empty list
        session.setdefault('selected_prerequisites', [])

        # Fetch blocks
        curs.execute("SELECT DISTINCT number FROM Block ORDER BY number")
        blocks = [record[0] for record in curs.fetchall()]

        # Fetch professors
        curs.execute("SELECT DISTINCT name FROM Professor ORDER BY name")
        professor = [record[0] for record in curs.fetchall()]

        # Fetch exam types
        curs.execute("SELECT DISTINCT name FROM ExamType ORDER BY name")
        exam_type = [record[0] for record in curs.fetchall()]   

        # fetch ects
        curs.execute("SELECT DISTINCT ECTS FROM Course ORDER BY ECTS")
        ects = [record[0] for record in curs.fetchall()]

        # fetch prerequisites
        curs.execute("SELECT DISTINCT name FROM Course ORDER BY name")
        prerequisites = [record[0] for record in curs.fetchall()]

        # fetch duration
        curs.execute("SELECT DISTINCT duration FROM Course ORDER BY duration")
        duration = [record[0] for record in curs.fetchall()]

        # Join tables to fetch course data 
        query = """
            SELECT c.name, b.number AS block, c.duration, array_agg(pr.name) AS prerequisites, 
            p.name AS professor, cr.average_grade, et.name AS exam_type, c.ECTS, cas.average_score, c.id
            FROM Course c
            LEFT JOIN CoursePrerequisite cp ON cp.course_id = c.id
            LEFT JOIN Course pr ON pr.id = cp.prerequisite_course_id
            LEFT JOIN CourseProfessor s ON s.course_id = c.id
            LEFT JOIN Professor p ON p.id = s.professor_id
            LEFT JOIN CourseResult cr ON cr.course_id = c.id
            LEFT JOIN CourseExamType cet ON cet.course_id = c.id
            LEFT JOIN ExamType et ON et.id = cet.exam_type_id
            LEFT JOIN CourseBlock cb ON cb.course_id = c.id
            LEFT JOIN Block b ON b.number = cb.block_number
            LEFT JOIN CourseAverageScores cas ON cas.course_id = c.id
        """
        # query_conditions is a list of conditions 
        query_conditions = []

        if 'selected_prerequisites' not in session or not session['selected_prerequisites']:
            session['selected_prerequisites'] = []

        # init params as an empty list
        params = []
        # if request is post then get the selected values from the form
        if request.method == 'POST':
            selected_block = request.form.get('block')
            selected_professor = request.form.get('professor')
            selected_exam_type = request.form.get('exam_type')
            selected_grade = request.form.get('grade')
            selected_ects = request.form.get('ects')
            selected_duration = request.form.get('duration')
            selected_course_name = request.form.get('course_name')
            selected_min_score = request.form.get('min_score')
            exclude_prerequisite = 'exclude_prerequisite' in request.form

            session.modified = True  # This line is needed because mutable session data might not trigger a save

            # Add a condition for each selected filter
            if selected_block and selected_block != 'None':
                query_conditions.append(f"b.number = {selected_block}")

            if selected_professor and selected_professor != 'None':
                query_conditions.append(f"p.name = '{selected_professor}'")

            if selected_exam_type and selected_exam_type != 'None':
                query_conditions.append(f"et.name = '{selected_exam_type}'")

            if selected_grade:
                query_conditions.append(f"cr.average_grade >= {selected_grade}")

            if selected_ects and selected_ects != 'None':
                query_conditions.append(f"c.ECTS = {selected_ects}")

            if selected_duration and selected_duration != 'None':
                query_conditions.append(f"c.duration = {selected_duration}")

            if selected_min_score:
                query_conditions.append(f"cas.average_score >= {selected_min_score}")

            # Add a condition for the course name search
            if selected_course_name:
                query_conditions.append("c.name ILIKE %s")
                params.append(f"%{selected_course_name}%")

            # get the selected prerequisites from the existing session
            selected_prerequisites = session.get('selected_prerequisites', [])

            # this might not be needed
            exclude_prerequisite = 'exclude_prerequisite' in request.form

            # init prerequisite_conditions as an empty list
            prerequisite_conditions = []

            # If selected_prerequisites is not empty loop through the selected_prerequisites and add a condition for each prerequisite
            if selected_prerequisites:
                for prerequisite in selected_prerequisites:
                    prerequisite_condition = """
                    EXISTS (
                        SELECT 1 
                        FROM CoursePrerequisite cp 
                        JOIN Course pr ON cp.prerequisite_course_id = pr.id 
                        WHERE cp.course_id = c.id AND pr.name = '%s'
                    )
                    """ % prerequisite
                    if exclude_prerequisite:
                        prerequisite_condition = "NOT " + prerequisite_condition
                    prerequisite_conditions.append(prerequisite_condition)
                query_conditions.append("(" + " OR ".join(prerequisite_conditions) + ")")

        # query_conditions is not empty then add WHERE + query conditions joined by AND  
        if query_conditions:
            query += " WHERE " + " AND ".join(query_conditions)

        # Add GROUP BY clause to the query
        query += """
            GROUP BY c.id, b.number, p.name, cr.average_grade, et.name, c.ECTS, cas.average_score
        """
        # execute the query with the params
        curs.execute(query, params)
        data = curs.fetchall()
        conn.close()
        
        # render the template with the data
        return render_template(
            'home.html', 
            data=data, 
            blocks=blocks, 
            professors=professor, 
            exam_types=exam_type,
            ects=ects, 
            durations=duration, 
            prerequisites=prerequisites, 
            selected_prerequisites=session['selected_prerequisites'], 
            form=request.form
            )

    # Handle prerequisites form submission
    @app.route('/prerequisites', methods=['POST'])
    def prerequisites():
        # get the selected prerequisite from the form
        selected_prerequisite = request.form.get('prerequisite', '')  
        action = request.form.get('action')

        # if the selected prerequisite is not empty or None then add it to the session
        if selected_prerequisite != '' and selected_prerequisite is not None:
            # if action is Add then add the selected prerequisite to the session
            if action == 'Add': 
                if 'selected_prerequisites' not in session:
                    session['selected_prerequisites'] = [selected_prerequisite]
                else:
                    session['selected_prerequisites'].append(selected_prerequisite)
            # if action is Remove then remove the selected prerequisite from the session
            elif action == 'Remove' and 'selected_prerequisites' in session:  
                if selected_prerequisite in session['selected_prerequisites']:
                    session['selected_prerequisites'].remove(selected_prerequisite)
        # maybe add user feedback in flash here            
        else:
            print("Selected prerequisite is empty or None.")

        session.modified = True # session has been modified so set modified to True
        
        return redirect(url_for('home'))
    
    # Handle completed courses form submission
    @app.route('/load_completed_courses', methods=['POST'])
    def load_completed_courses():
        conn = get_db_conn()
        curs = conn.cursor()

        # Query to fetch completed courses for the current user
        query = """
            SELECT c.name 
            FROM CompletedCourses cc
            JOIN Course c ON cc.course_id = c.id
            WHERE cc.student_id = %s
        """
        curs.execute(query, [current_user.id])
        completed_courses = [record[0] for record in curs.fetchall()]
        conn.close()

        # Add the completed courses to the session
        if 'selected_prerequisites' not in session:
            session['selected_prerequisites'] = completed_courses
        else:
            session['selected_prerequisites'].extend(completed_courses)
        session['selected_prerequisites'] = list(set(session['selected_prerequisites']))  # Remove duplicates

        session.modified = True

        return redirect(url_for('home'))