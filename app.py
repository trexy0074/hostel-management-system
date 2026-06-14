from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hostel_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register")
def register():
    return render_template("register.html")


# ---------------- LOGIN (SESSION ENABLED) ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        session["user"] = username
        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- DASHBOARD (DYNAMIC) ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hostel.db")
    cur = conn.cursor()

    # total users
    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    # complaints count (safe)
    try:
        cur.execute("SELECT COUNT(*) FROM complaints")
        complaints = cur.fetchone()[0]
    except:
        complaints = 0

    conn.close()

    return render_template(
        "dashboard.html",
        users=users,
        complaints=complaints
    )


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html")


# ---------------- BOOK HOSTEL ----------------
@app.route("/book-hostel")
def book_hostel():
    return render_template("book_hostel.html")


# ---------------- ROOM DETAILS ----------------
@app.route("/room-details")
def room_details():
    return render_template("room_details.html")


# ---------------- COMPLAINT ----------------
@app.route("/complaint")
def complaint():
    return render_template("complaint.html")


# ---------------- FEEDBACK ----------------
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


# ---------------- CHANGE PASSWORD ----------------
@app.route("/change-password")
def change_password():
    return render_template("change_password.html")


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


# ---------------- REGISTERED COMPLAINT ----------------
@app.route("/registered-complaint")
def registered_complaint():
    return render_template("registered_complaint.html")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)