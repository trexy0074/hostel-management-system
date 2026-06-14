import sqlite3

conn = sqlite3.connect("hostel.db")
cursor = conn.cursor()

# Student
cursor.execute("""
INSERT INTO Student
(Student_Name, Gender, Contact_Number, Email, Course, Address, Room_ID)
VALUES
('Rahul Sharma','Male','9876543210','rahul@example.com','BCA','Delhi',1)
""")

# Room
cursor.execute("""
INSERT INTO Room
(Room_Number, Room_Type, Capacity, Occupied_Beds, Room_Status)
VALUES
('A101','Single',1,1,'Occupied')
""")

# Fee Details
cursor.execute("""
INSERT INTO Fee_Details
(Student_ID, Amount, Payment_Date, Payment_Mode, Payment_Status)
VALUES
(1,25000,'2026-06-15','Online','Paid')
""")

# Complaint
cursor.execute("""
INSERT INTO Complaint
(Student_ID, Complaint_Type, Complaint_Details, Complaint_Date, Status)
VALUES
(1,'Electricity','Fan not working','2026-06-15','Pending')
""")

# Visitor
cursor.execute("""
INSERT INTO Visitor
(Visitor_Name, Student_ID, Visit_Purpose, Entry_Time, Exit_Time)
VALUES
('Amit Sharma',1,'Meeting','2026-06-15 10:00','2026-06-15 11:00')
""")

# Hostel Staff
cursor.execute("""
INSERT INTO Hostel_Staff
(Staff_Name, Designation, Contact_Number, Email)
VALUES
('Rajesh Kumar','Warden','9999999999','warden@hostel.com')
""")

# User Account
cursor.execute("""
INSERT INTO User_Account
(Username, Password, User_Role, Last_Login)
VALUES
('rahul','password123','Student','2026-06-15 09:00')
""")

# Room Allocation
cursor.execute("""
INSERT INTO Room_Allocation
(Student_ID, Room_ID, Allocation_Date, Allocation_Status)
VALUES
(1,1,'2026-06-15','Allocated')
""")

conn.commit()
conn.close()

print("Sample Data Inserted")