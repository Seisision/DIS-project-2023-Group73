-- Professor
INSERT INTO Professor (name) VALUES ('John Doe'), ('Jane Smith'), ('Robert Johnson');

-- Role
INSERT INTO Role (name) VALUES ('Professor'), ('Assistant'), ('Lecturer');

-- Course
INSERT INTO Course (duration, ECTS, name) VALUES (1, 6, 'Physics 101');
INSERT INTO Course (duration, ECTS, name, prerequesite_course_id) VALUES (1, 6, 'Physics 102', 1);

-- Review
INSERT INTO Review (year, score, text, course_id) VALUES (2023, 5, 'Great course!', 1), (2023, 3, 'Difficult, but rewarding.', 2);

-- Student
INSERT INTO Student (name) VALUES ('Student A'), ('Student B'), ('Student C');

-- Block
INSERT INTO Block (number) VALUES (1), (2), (3);

-- ExamType
INSERT INTO ExamType (name) VALUES ('Written'), ('Oral'), ('Practical');

-- CourseResult
INSERT INTO CourseResult (average_grade, year, course_id) VALUES (3.5, 2023, 1), (2.5, 2023, 2);

-- Staff
INSERT INTO Staff (professor_id, role_id, course_id) VALUES (1, 1, 1), (2, 2, 2), (3, 3, 1);

-- CourseExamType
INSERT INTO CourseExamType (course_id, exam_type_id) VALUES (1, 1), (2, 2), (1, 3);

-- CourseBlock
INSERT INTO CourseBlock (course_id, block_number) VALUES (1, 1), (2, 2);

-- StudentReview
INSERT INTO StudentReview (student_id, review_id) VALUES (1, 1), (2, 2);
