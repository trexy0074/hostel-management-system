from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hostel_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("hostel.db")
        cur = conn.cursor()

        # FIX: prevent duplicate users
        cur.execute("SELECT * FROM User_Account WHERE Username=?", (username,))
        if cur.fetchone():
            conn.close()
            return "Username already exists"

        cur.execute("""
            INSERT INTO User_Account (Username, Password, User_Role, Last_Login)
            VALUES (?, ?, ?, ?)
        """, (username, password, "Student", None))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("auth/register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("hostel.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT User_ID, Username, User_Role
            FROM User_Account
            WHERE Username=? AND Password=?
        """, (username, password))

        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[2]

            cur.execute("""
                UPDATE User_Account
                SET Last_Login=?
                WHERE User_ID=?
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0]))

            conn.commit()
            conn.close()

            if user[2] == "Admin":
                return redirect("/admin")
            return redirect("/dashboard")

        conn.close()
        return "Invalid username or password"

    return render_template("auth/login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Student")
    students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Complaint")
    complaints = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Room")
    rooms = cur.fetchone()[0]

    conn.close()

    return render_template(
        "student/dashboard.html",
        students=students,
        complaints=complaints,
        rooms=rooms,
        username=session["username"],
        role=session["role"]
    )


# ---------------- STUDENT REGISTER ----------------
@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        conn = sqlite3.connect("hostel.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Student
            (Student_Name, Gender, Contact_Number, Email, Course, Address, Room_ID)
            VALUES (?, ?, ?, ?, ?, ?, NULL)
        """, (
            request.form["name"],
            request.form["gender"],
            request.form["phone"],
            request.form["email"],
            request.form["course"],
            request.form["address"]
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("student/register_student.html")


# ---------------- ROOM DETAILS ----------------
@app.route("/room-details")
def room_details():
    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Room")
    rooms = cur.fetchall()

    conn.close()

    return render_template("student/room_details.html", rooms=rooms)


# ---------------- BOOK HOSTEL ----------------
@app.route("/book-hostel")
def book_hostel():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("student/book_hostel.html")


# ---------------- COMPLAINT ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = sqlite3.connect("hostel.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Complaint
            (Student_ID, Complaint_Type, Complaint_Details, Complaint_Date, Status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            request.form["type"],
            request.form["details"],
            datetime.now().strftime("%Y-%m-%d"),
            "Pending"
        ))

        conn.commit()
        conn.close()

        return redirect("/my-complaints")

    return render_template("student/complaint.html")


# ---------------- MY COMPLAINTS ----------------
@app.route("/my-complaints")
def my_complaints():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM Complaint
        WHERE Student_ID=?
    """, (session["user_id"],))

    complaints = cur.fetchall()
    conn.close()

    return render_template("student/my_complaints.html", complaints=complaints)


# ---------------- FEEDBACK ----------------
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        return redirect("/dashboard")

    return render_template("student/feedback.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin_panel():
    if "user_id" not in session or session.get("role") != "Admin":
        return "Access Denied"

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("SELECT User_ID, Username, User_Role FROM User_Account")
    users = cur.fetchall()

    cur.execute("SELECT * FROM Complaint")
    complaints = cur.fetchall()

    cur.execute("SELECT * FROM Room")
    rooms = cur.fetchall()

    conn.close()

    return render_template("admin/admin.html",
                           users=users,
                           complaints=complaints,
                           rooms=rooms)


# ---------------- DELETE USER ----------------
@app.route("/admin/delete-user/<int:user_id>")
def delete_user(user_id):
    if session.get("role") != "Admin":
        return "Access Denied"

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM User_Account WHERE User_ID=?", (user_id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- DELETE COMPLAINT ----------------
@app.route("/admin/delete-complaint/<int:cid>")
def delete_complaint(cid):
    if session.get("role") != "Admin":
        return "Access Denied"

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM Complaint WHERE Complaint_ID=?", (cid,))
    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- RESOLVE ----------------
@app.route("/admin/resolve-complaint/<int:cid>")
def resolve_complaint(cid):
    if session.get("role") != "Admin":
        return "Access Denied"

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE Complaint
        SET Status='Resolved'
        WHERE Complaint_ID=?
    """, (cid,))

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)