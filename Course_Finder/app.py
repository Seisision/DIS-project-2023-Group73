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

@app.route('/')
def home():
    conn = get_db_conn()
    curs = conn.cursor()

    # Join tables to fetch course data
    curs.execute("""
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
    """)

    data = curs.fetchall()

    conn.close()

    return render_template('home.html', data=data)

