import sqlite3

conn = sqlite3.connect("hostel.db")
cursor = conn.cursor()

# ---------------- STUDENT ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student(
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_Name TEXT,
    Gender TEXT,
    Contact_Number TEXT,
    Email TEXT,
    Course TEXT,
    Address TEXT,
    Room_ID INTEGER
)
""")

# ---------------- ROOM ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Room(
    Room_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Room_Number TEXT,
    Room_Type TEXT,
    Capacity INTEGER,
    Occupied_Beds INTEGER DEFAULT 0,
    Room_Status TEXT
)
""")

# ---------------- FEE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Fee_Details(
    Fee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER,
    Amount REAL,
    Payment_Date TEXT,
    Payment_Mode TEXT,
    Payment_Status TEXT
)
""")

# ---------------- COMPLAINT ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Complaint(
    Complaint_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER,
    Complaint_Type TEXT,
    Complaint_Details TEXT,
    Complaint_Date TEXT,
    Status TEXT DEFAULT 'Pending'
)
""")

# ---------------- VISITOR ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Visitor(
    Visitor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Visitor_Name TEXT,
    Student_ID INTEGER,
    Visit_Purpose TEXT,
    Entry_Time TEXT,
    Exit_Time TEXT
)
""")

# ---------------- STAFF ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Hostel_Staff(
    Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Staff_Name TEXT,
    Designation TEXT,
    Contact_Number TEXT,
    Email TEXT
)
""")

# ---------------- USER ACCOUNT (USED FOR LOGIN) ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS User_Account(
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE,
    Password TEXT,
    User_Role TEXT DEFAULT 'Student',
    Last_Login TEXT
)
""")

# ---------------- ROOM ALLOCATION ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Room_Allocation(
    Allocation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER,
    Room_ID INTEGER,
    Allocation_Date TEXT,
    Allocation_Status TEXT DEFAULT 'Active'
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")