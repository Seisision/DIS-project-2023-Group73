from flask import render_template, request, session, redirect, url_for

def init_home(app, get_db_conn):

    @app.route('/', methods=['GET', 'POST'])
    def home():
        conn = get_db_conn()
        curs = conn.cursor()

        session.setdefault('selected_prerequisites', [])
        print(f"Home route: Selected prerequisites session: {session.get('selected_prerequisites', [])}")

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
            SELECT c.name, b.number AS block, c.duration, array_agg(pr.name) AS prerequisites, p.name AS professor, cr.average_grade, et.name AS exam_type, c.ECTS, c.id
            FROM Course c
            LEFT JOIN CoursePrerequisite cp ON cp.course_id = c.id
            LEFT JOIN Course pr ON pr.id = cp.prerequisite_course_id
            LEFT JOIN Staff s ON s.course_id = c.id
            LEFT JOIN Professor p ON p.id = s.professor_id
            LEFT JOIN CourseResult cr ON cr.course_id = c.id
            LEFT JOIN CourseExamType cet ON cet.course_id = c.id
            LEFT JOIN ExamType et ON et.id = cet.exam_type_id
            LEFT JOIN CourseBlock cb ON cb.course_id = c.id
            LEFT JOIN Block b ON b.number = cb.block_number
        """
        query_conditions = []

        if 'selected_prerequisites' not in session or not session['selected_prerequisites']:
            session['selected_prerequisites'] = []

        # Handle filtering form submission
        # Retrieve filtering criteria from the request object
        # Construct the SQL query with the filtering conditions
        # Execute the query and fetch the filtered data
        # Assign the filtered data to a variable for rendering
        params = []
        if request.method == 'POST':
            selected_block = request.form.get('block')
            selected_professor = request.form.get('professor')
            selected_exam_type = request.form.get('exam_type')
            selected_grade = request.form.get('grade')
            selected_ects = request.form.get('ects')
            selected_duration = request.form.get('duration')
            selected_course_name = request.form.get('course_name')
            exclude_prerequisite = 'exclude_prerequisite' in request.form


            session.modified = True  # This line is needed because mutable session data might not trigger a save

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

            # Add a condition for the course name search
            if selected_course_name:
                query_conditions.append("c.name ILIKE %s")
                params.append(f"%{selected_course_name}%")


            selected_prerequisites = session.get('selected_prerequisites', [])
            exclude_prerequisite = 'exclude_prerequisite' in request.form

            # If selected_prerequisites is not empty
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
                    query_conditions.append(prerequisite_condition)
                    
        if query_conditions:
            query += " WHERE " + " AND ".join(query_conditions)

        query += """
            GROUP BY c.id, b.number, p.name, cr.average_grade, et.name
        """

        curs.execute(query, params)
        data = curs.fetchall()
        conn.close()

        print(f"Home route: Selected prerequisites session: {session['selected_prerequisites']}")

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

    @app.route('/prerequisites', methods=['POST'])
    def prerequisites():
        selected_prerequisite = request.form.get('prerequisite', '')  
        action = request.form.get('action')

        print("Received prerequisite: ", selected_prerequisite)
        print("Received action: ", action)

        if selected_prerequisite != '' and selected_prerequisite is not None:
            print("Selected prerequisite is non-empty and not None.")
            if action == 'Add':  # change 'add' to 'Add'
                print("Adding prerequisite...")
                if 'selected_prerequisites' not in session:
                    print("Session['selected_prerequisites'] does not exist, creating...")
                    session['selected_prerequisites'] = [selected_prerequisite]
                else:
                    print("Session['selected_prerequisites'] exists, appending...")
                    session['selected_prerequisites'].append(selected_prerequisite)
                print("Added prerequisite, session is now: ", session['selected_prerequisites'])
            elif action == 'Remove' and 'selected_prerequisites' in session:  # change 'remove' to 'Remove'
                if selected_prerequisite in session['selected_prerequisites']:
                    session['selected_prerequisites'].remove(selected_prerequisite)
                print("Removed prerequisite, session is now: ", session['selected_prerequisites'])
        else:
            print("Selected prerequisite is empty or None.")

        session.modified = True

        return redirect(url_for('home'))