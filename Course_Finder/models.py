class Student:
    def __init__(self, id=None, username=None, password_hash=None, name=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.name = name
    
    # These properties are required by Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def select_Student_by_id(id, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT * FROM Student
    WHERE id = %s
    """
    cur.execute(sql, (id,))
    user = Student(*cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    conn.close()
    return user

def select_Student_by_username(username, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT * FROM Student
    WHERE username = %s
    """
    cur.execute(sql, (username,))
    user = Student(*cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    conn.close()
    return user

def save_student(student, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO Student (username, password_hash, name)
    VALUES (%s, %s, %s)
    RETURNING id
    """
    cur.execute(sql, (student.username, student.password_hash, student.name))
    student_id = cur.fetchone()[0]  # Retrieve the generated student ID
    conn.commit()
    cur.close()
    conn.close()
    student.id = student_id  # Assign the generated ID to the student object

def select_Course_by_name(name, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT * FROM Course
    WHERE name = %s
    """
    cur.execute(sql, (name,))
    course = cur.fetchone()
    cur.close()
    conn.close()
    return course

def save_completed_course(student_id, course_id, completion_date, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO CompletedCourses (student_id, course_id, completion_date)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (student_id, course_id, completion_date))
    conn.commit()
    cur.close()
    conn.close()

def delete_student_completed_course(student_id, course_id, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    DELETE FROM CompletedCourses
    WHERE student_id = %s AND course_id = %s
    """
    cur.execute(sql, (student_id, course_id))
    conn.commit()
    cur.close()
    conn.close()

def get_completed_courses(student_id, get_db_conn):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT Course.name, CompletedCourses.completion_date, Course.id 
    FROM CompletedCourses 
    INNER JOIN Course ON CompletedCourses.course_id = Course.id
    WHERE CompletedCourses.student_id = %s
    """
    cur.execute(sql, (student_id,))
    completed_courses = cur.fetchall()
    cur.close()
    conn.close()
    return completed_courses
