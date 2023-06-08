CREATE TABLE Professor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Course (
    id SERIAL PRIMARY KEY,
    duration INT NOT NULL,
    ECTS FLOAT NOT NULL,
    name VARCHAR(100) NOT NULL,
    prerequisite_course_id INT, 
    FOREIGN KEY (prerequisite_course_id) REFERENCES Course(id) 
);

CREATE TABLE CoursePrerequisite (
    course_id INT NOT NULL,
    prerequisite_course_id INT NOT NULL,
    PRIMARY KEY (course_id, prerequisite_course_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (prerequisite_course_id) REFERENCES Course(id)
);


CREATE TABLE Review (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    score INT NOT NULL,
    text TEXT,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id) 
);

CREATE TABLE Student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Block (
    number INT PRIMARY KEY
);

CREATE TABLE ExamType (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE CourseResult (
    id SERIAL PRIMARY KEY,
    average_grade FLOAT,
    year INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id) 
);

CREATE TABLE Staff (
    professor_id INT NOT NULL,
    role_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (professor_id, role_id, course_id),
    FOREIGN KEY (professor_id) REFERENCES Professor(id),
    FOREIGN KEY (role_id) REFERENCES Role(id),
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE CourseExamType (
    course_id INT NOT NULL,
    exam_type_id INT NOT NULL,
    PRIMARY KEY (course_id, exam_type_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (exam_type_id) REFERENCES ExamType(id)
);

CREATE TABLE CourseBlock (
    course_id INT NOT NULL,
    block_number INT NOT NULL,
    PRIMARY KEY (course_id, block_number),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (block_number) REFERENCES Block(number)
);

CREATE TABLE StudentReview (
    student_id INT NOT NULL,
    review_id INT NOT NULL,
    PRIMARY KEY (student_id, review_id),
    FOREIGN KEY (student_id) REFERENCES Student(id),
    FOREIGN KEY (review_id) REFERENCES Review(id)
);
