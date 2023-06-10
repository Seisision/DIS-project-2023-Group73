class Student:
    def __init__(self, student_tuple):
        self.id = student_tuple[0]
        self.username = student_tuple[1]
        self.password_hash = student_tuple[2]
        self.name = student_tuple[3]
    
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
    user = Student(cur.fetchone()) if cur.rowcount > 0 else None
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
    user = Student(cur.fetchone()) if cur.rowcount > 0 else None
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
