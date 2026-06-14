import sqlite3

conn = sqlite3.connect("hostel.db")
cur = conn.cursor()

cur.execute("SELECT * FROM User_Account")
users = cur.fetchall()

for u in users:
    print(u)

conn.close()