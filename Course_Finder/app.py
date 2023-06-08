from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# gamle Database connection settings
#host="127.0.0.1"
#database="Course Finder"
#user="postgres"
#password="dis"

# Database connection settings til testing (ulrik)
# det her er lidt en cringem måde at gøre det på,
# men jeg tror de originale settings er gemt ovenfor?

host="127.0.0.1"
database="postgres"
user="postgres"
password="dis"
port=1333

def get_db_conn():
    return psycopg2.connect(
        host=host, 
        database=database, 
        user=user, 
        password=password,
        port=port,
    )

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db_conn()
    curs = conn.cursor()

    # Join tables to fetch course data
    query = """
        SELECT c.name, b.number AS block, c.duration, array_agg(pr.name) AS prerequisites, p.name AS professor, cr.average_grade, et.name AS exam_type, c.ECTS
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
        GROUP BY c.id, b.number, p.name, cr.average_grade, et.name
    """

    if request.method == 'POST':
        # Handle filtering form submission
        # Retrieve filtering criteria from the request object
        # Construct the SQL query with the filtering conditions
        # Execute the query and fetch the filtered data
        # Assign the filtered data to a variable for rendering
        selected_block = request.form.get('block')
        selected_professor = request.form.get('professor')
        selected_exam_type = request.form.get('exam_type')
        selected_grade = request.form.get('grade')
        selected_ects = request.form.get('ects')
        selected_duration = request.form.get('duration')
        selected_prerequisite = request.form.get('prerequisite')

        if selected_block:
            query += f" AND b.number = {selected_block}"
        if selected_professor:
            query += f" AND p.name = '{selected_professor}'"
        if selected_exam_type:
            query += f" AND et.name = '{selected_exam_type}'"
        if selected_grade:
            query += f" AND cr.average_grade >= {selected_grade}"
        if selected_ects:
            query += f" AND c.ECTS = {selected_ects}"
        if selected_duration:
            query += f" AND c.duration = {selected_duration}"
        if selected_prerequisite:
            query += f" AND pr.name = '{selected_prerequisite}'"

    curs.execute(query)
    data = curs.fetchall()
    conn.close()

    return render_template('home.html', data=data)

