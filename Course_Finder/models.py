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

