# DIS-project-2023-Group73
Repository for the group project for the DIS 2023 course. The project is  web-app (website) that interacts with a database.

Search courses by: 
Block, Professor, Exam Type, Minimum average grade, Minimum average review score, ECTS points, Duration, Course names, Prerequisite courses.

You can see reviews of courses and write reviews of courses.

(assumes a working python and pip)

# running the course-finder project

(1) Install the dependencies like below:
>$ pip install -r requirements.txt

(2) Set up your database by running the relevant SQL files (schema.sql followed by init_schema.sql). schema creates the tables and init populates them with test data.


(3) In app.py on lines 22-27 set your own database settings (ip,database,user,password,port).

(4) Run the webapp using the following
>$ python Course_Finder/app.py


------------------------------------------------------------------------------------------------------------------------------------------------------
# Guide to the Course_Finder Web Application

## Overview

The Course_Finder application allows users to filter courses based on parameters including **Block**, **Professor**, **Exam Type**, **Minimum Average Grade**, **Minimum Average Review Score**, **ECTS points**, **Duration**, **Course Names**, and **Prerequisite Courses**. User accounts can be created via the registration functionality, accessible from the 'Login' page. 

## User Account Functionality

Upon successful login, users have access to additional features:

1. **My Reviews**: This section displays all reviews written by the user, offering the functionality to edit or delete these reviews.

2. **Write a Review**: This feature enables users to author a review for any course listed as completed. Note that users are limited to one review per course, and any amendments must be done through the "My Reviews" section.

3. **Completed Courses**: This section allows users to manage their list of completed courses, with the ability to add or remove courses as needed.

## Review Viewing

Within the course information table on the homepage, the 'View Reviews' button redirects users to a page displaying all reviews of the respective course.
