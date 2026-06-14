import sqlite3

conn = sqlite3.connect("hostel.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO User_Account (Username, Password, User_Role)
VALUES ('admin', 'admin123', 'Admin')
""")

conn.commit()
conn.close()

print("Admin user created")