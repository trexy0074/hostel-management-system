from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hostel_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER (REAL DB LOGIN SYSTEM) ----------------
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


# ---------------- LOGIN (REAL AUTH USING USER_ACCOUNT) ----------------
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

            # update last login
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


# ---------------- DASHBOARD (DYNAMIC REAL DATA) ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    # real data from your database
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


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("profile.html")


# ---------------- OTHER PAGES (UNCHANGED UI PAGES) ----------------
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


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)