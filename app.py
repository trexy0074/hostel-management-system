from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

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

if __name__ == "__main__":
    app.run(debug=True)