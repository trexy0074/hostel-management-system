Overview

The Hostel Management System is a web-based application designed to simplify and automate hostel operations. It manages student records, room allocation, and administrative tasks in a structured and efficient manner. The system reduces manual effort and improves accuracy in hostel management workflows.

Key Features
Admin Panel
Secure admin authentication
Add, update, and delete student records
Manage rooms and allocations
Track hostel occupancy and availability
View complete student information
Student Panel
Student registration and login
View allocated room details
Update personal profile
Access hostel-related information
Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: PHP
Database: MySQL
Server Environment: Apache (XAMPP / WAMP / LAMP)
Installation Guide

Step 1: Clone the Repository
git clone https://github.com/trexy0074/hostel-management-system.

Step 2: Move to Server Directory
XAMPP: htdocs
WAMP: www

Step 3: Start Server

Start Apache and MySQL using XAMPP/WAMP control panel.

Step 4: Setup Database
Open phpMyAdmin
Create database: hostel
Import SQL file from /database folder

Step 5: Run Project

Open browser and go to:

http://localhost/hostel-management-system

Project Structure

hostel-management-system/
│
├── admin/          Admin panel files
├── student/        Student module files
├── assets/         CSS, JS, images
├── database/       SQL database file
├── config/         Database configuration
└── index.php       Entry point

Future Enhancements
Online fee payment integration
Complaint and grievance system
Email and SMS notifications
Improved responsive UI
Role-based access control system

Author

Developed as an academic project for learning and demonstration purposes.

License

This project is intended for educational use only.
