-- Clear existing data

DELETE FROM StudentReview;
DELETE FROM CourseBlock;
DELETE FROM CourseExamType;
DELETE FROM Staff;
DELETE FROM CourseResult;
DELETE FROM ExamType;
DELETE FROM Block;
DELETE FROM Student;
DELETE FROM Review;
DELETE FROM CoursePrerequisite;
DELETE FROM Course;
DELETE FROM Role;
DELETE FROM Professor;
-- Now insert data

-- Insert professors
INSERT INTO Professor (id, name) VALUES 
(1, 'Jon Sporring'), 
(2, 'Rasmus Pagh'), 
(3, 'Boris'),
(4, 'Kasper Hornbæk'), 
(5, 'Henrik'), 
(6, 'Troels'),
(7, 'Stefan'),
(8, 'bulat'),
(9, 'Pawel Destroyer of Grades'),
(10, 'Dmitriy');

-- Insert roles
INSERT INTO Role (id, name) VALUES 
(1, 'Lecturer'), 
(2, 'Assistant'), 
(3, 'Adjunct'),
(4, 'Professor'), 
(5, 'Assistant'), 
(6, 'Lecturer');

INSERT INTO Course (id, duration, ECTS, name) VALUES 
(1, 2, 15, 'Programmering og problemløsning'),
(2, 2, 15, 'Diskret matematik og algoritmer'),
(3, 2, 15, 'Softwareudvikling'),
(4, 1, 7.5, 'Interaktionsdesign'),
(5, 1, 7.5, 'Lineær algebra i datalogi'),
(6, 2, 15, 'Computersystemer'),
(7, 1, 7.5, 'Matematisk analyse og sandsynligheds-teori i datalogi'),
(8, 1, 7.5, 'Modelling and Analysis of Data'),
(9, 1, 7.5, 'Algoritmer og datastrukturer'),
(10, 1, 7.5, 'Databases and Information Systems');

INSERT INTO CoursePrerequisite (course_id, prerequisite_course_id) VALUES
(3, 1),
(5, 1),
(5, 2),
(6, 2),
(8, 7),
(8, 5),
(9, 2),
(10, 6),
(10,  )

-- Review
INSERT INTO Review (id, year, score, text, course_id) VALUES 
(1, 2023, 5, 'Great Course!', 1),
(2, 2023, 4, 'Challenging but good.', 2),
(3, 2023, 5, 'Very useful.', 3),
(4, 2023, 5, 'Hard but rewarding.', 4),
(5, 2023, 4, 'Informative.', 5),
(6, 2023, 4, 'Great for understanding data.', 10),
(7, 2023, 5, 'Great course!', 7); 

-- Student
INSERT INTO Student (id, name) VALUES 
(1, 'Student A'),
(2, 'Student B'),
(3, 'Student C'),
(4, 'Student D'),
(5, 'Student E'),
(6, 'Student F');

-- Block
INSERT INTO Block (number) VALUES 
(1), 
(2), 
(3), 
(4);

-- ExamType
INSERT INTO ExamType (id, name) VALUES 
(1, 'Written under invigilation'), 
(2, 'Oral'), 
(3, 'Written assignment'),
(4, 'continuous assessment');

-- CourseResult
INSERT INTO CourseResult (id, average_grade, year, course_id) VALUES 
(1, NULL, 2023, 1),
(2, NULL, 2023, 2),
(3, 7, 2023, 3),
(4, 10, 2023, 4),
(5, 5, 2023, 5),
(6, 6, 2023, 6),
(7, 5, 2023, 7),
(8, 5, 2023, 8),
(9, 3, 2023, 9),
(10, 7, 2023, 10);

-- Staff
INSERT INTO Staff (professor_id, role_id, course_id) VALUES 
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 2, 4),
(5, 3, 5),
(6, 3, 6),
(7, 3, 7),
(8, 3, 8),
(9, 3, 9),
(10, 3, 10);

-- CourseExamType
INSERT INTO CourseExamType (course_id, exam_type_id) VALUES 
(1, 4),
(2, 4),
(3, 3),
(4, 2),
(5, 1),
(6, 1),
(7, 4),
(8, 2),
(9, 1),
(10, 1);


INSERT INTO CourseBlock (course_id, block_number) VALUES 
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 1),
(7, 1),
(8, 2),
(9, 3),
(10, 4);

INSERT INTO StudentReview (student_id, review_id) VALUES 
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7);