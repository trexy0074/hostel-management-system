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

        try:
            cur.execute("""
                INSERT INTO User_Account (Username, Password, User_Role)
                VALUES (?, ?, ?)
            """, (username, password, "Student"))

            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


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

            return redirect("/dashboard")

        conn.close()
        return "Invalid username or password"

    return render_template("login.html")


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
        "dashboard.html",
        students=students,
        complaints=complaints,
        rooms=rooms,
        username=session["username"],
        role=session["role"]
    )


# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin_panel():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Admin":
        return "Access Denied"

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    cur.execute("SELECT User_ID, Username, User_Role FROM User_Account")
    users = cur.fetchall()

    cur.execute("SELECT Complaint_ID, Student_ID, Complaint_Type, Status FROM Complaint")
    complaints = cur.fetchall()

    cur.execute("SELECT Room_ID, Room_Number, Room_Type, Room_Status FROM Room")
    rooms = cur.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        complaints=complaints,
        rooms=rooms
    )


# ---------------- 🔥 DELETE USER ----------------
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


# ---------------- 🔥 DELETE COMPLAINT ----------------
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


# ---------------- 🔥 RESOLVE COMPLAINT ----------------
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


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("profile.html")


# ---------------- OTHER PAGES ----------------
@app.route("/book-hostel")
def book_hostel():
    return render_template("book_hostel.html")


@app.route("/room-details")
def room_details():
    return render_template("room_details.html")


@app.route("/complaint")
def complaint():
    return render_template("complaint.html")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/change-password")
def change_password():
    return render_template("change_password.html")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/registered-complaint")
def registered_complaint():
    return render_template("registered_complaint.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)