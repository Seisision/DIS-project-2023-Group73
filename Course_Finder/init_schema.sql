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
DELETE FROM Professor;
DELETE FROM CompletedCourses;

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
(10, 4);

INSERT INTO Student (id, username, password_hash, name) VALUES 
(1, 'student_a', 'password_hash_value', 'Student A'),
(2, 'student_b', 'password_hash_value', 'Student B'),
(3, 'student_c', 'password_hash_value', 'Student C'),
(4, 'student_d', 'password_hash_value', 'Student D'),
(5, 'student_e', 'password_hash_value', 'Student E'),
(6, 'student_f', 'password_hash_value', 'Student F');
SELECT setval('student_id_seq', (SELECT MAX(id) FROM Student));

INSERT INTO Review (id, year, score, text, course_id) VALUES 
(1, 2023, 5, 'Great Course!', 1),
(2, 2023, 4, 'Challenging but good.', 2),
(3, 2023, 5, 'Very useful.', 3),
(4, 2023, 5, 'Easy but easy.', 4),
(5, 2023, 4, 'Informative.', 5),
(6, 2023, 4, 'Great for understanding data.', 10),
(7, 2023, 5, 'Great course!', 7),
(8, 2023, 3, 'Useful but a bit difficult.', 1),
(9, 2023, 4, 'Enjoyable and educational.', 1),
(10, 2023, 5, 'Really helped with my programming skills.', 1),
(11, 2023, 4, 'The content was deep and comprehensive.', 2),
(12, 2023, 3, 'Bit hard to understand at times, but overall good.', 2),
(13, 2023, 5, 'Amazing course, really explained algorithms well.', 2),
(14, 2023, 4, 'Very practical!', 3),
(15, 2023, 3, 'A bit complex at times, but very rewarding.', 3),
(16, 2023, 5, 'Engaging course with excellent examples.', 3),
(17, 2023, 4, 'Very useful for getting to grips with data systems.', 10),
(18, 2023, 3, 'Great content, though could use more examples.', 10),
(19, 2023, 5, 'This course really clarified databases for me.', 10);
SELECT setval('review_id_seq', (SELECT MAX(id) FROM Review));

INSERT INTO Block (number) VALUES 
(1), 
(2), 
(3), 
(4);

INSERT INTO ExamType (id, name) VALUES 
(1, 'Written under invigilation'), 
(2, 'Oral'), 
(3, 'Written assignment'),
(4, 'continuous assessment');

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

INSERT INTO CourseProfessor (professor_id, course_id) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

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
(4, 7),
(1, 8),
(1, 9),
(2, 10),
(2, 11),
(3, 12),
(3, 13),
(4, 14),
(4, 15),
(5, 16),
(5, 17),
(6, 18),
(6, 19);