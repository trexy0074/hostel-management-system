import sqlite3

conn = sqlite3.connect("hostel.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Student(
Student_ID INTEGER PRIMARY KEY,
Student_Name TEXT,
Gender TEXT,
Contact_Number TEXT,
Email TEXT,
Course TEXT,
Address TEXT,
Room_ID INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Room(
Room_ID INTEGER PRIMARY KEY,
Room_Number TEXT,
Room_Type TEXT,
Capacity INTEGER,
Occupied_Beds INTEGER,
Room_Status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Fee_Details(
Fee_ID INTEGER PRIMARY KEY,
Student_ID INTEGER,
Amount REAL,
Payment_Date TEXT,
Payment_Mode TEXT,
Payment_Status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Complaint(
Complaint_ID INTEGER PRIMARY KEY,
Student_ID INTEGER,
Complaint_Type TEXT,
Complaint_Details TEXT,
Complaint_Date TEXT,
Status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Visitor(
Visitor_ID INTEGER PRIMARY KEY,
Visitor_Name TEXT,
Student_ID INTEGER,
Visit_Purpose TEXT,
Entry_Time TEXT,
Exit_Time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Hostel_Staff(
Staff_ID INTEGER PRIMARY KEY,
Staff_Name TEXT,
Designation TEXT,
Contact_Number TEXT,
Email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS User_Account(
User_ID INTEGER PRIMARY KEY,
Username TEXT,
Password TEXT,
User_Role TEXT,
Last_Login TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Room_Allocation(
Allocation_ID INTEGER PRIMARY KEY,
Student_ID INTEGER,
Room_ID INTEGER,
Allocation_Date TEXT,
Allocation_Status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")