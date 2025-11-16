from flask import Flask, render_template, request, redirect, session, jsonify
import json, os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# -------------------- USER DATABASE FILE --------------------
USER_DB = "users.json"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=4)


# -------------------- HOME PAGE --------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------- SIGNUP --------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    users = load_users()
    email = request.json.get("email")
    password = request.json.get("password")

    if email in users:
        return jsonify({"status": "exists"})

    users[email] = {"password": password}
    save_users(users)

    return jsonify({"status": "success"})


# -------------------- LOGIN --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    users = load_users()
    email = request.json.get("email")
    password = request.json.get("password")

    if email in users and users[email]["password"] == password:
        session["user"] = email
        return jsonify({"status": "success"})

    return jsonify({"status": "fail"})


# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user_email = session["user"]
    return render_template("dashboard.html", user_name=user_email.split("@")[0])


# -------------------- LOGOUT --------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------- READ BOOK PAGE --------------------
@app.route("/read-book/<int:book_id>")
def read_book(book_id):

    BOOKS = {
        1: {"title": "Introduction to Algorithms (CLRS)",
            "pdf": "https://ia800503.us.archive.org/28/items/IntroductionToAlgorithmsThirdEdition/Introduction%20to%20Algorithms%20-%20Third%20Edition.pdf"},

        2: {"title": "Computer Networks - Tanenbaum",
            "pdf": "https://ncert.nic.in/textbook/pdf/lecs1dd.zip"},

        3: {"title": "Operating System Concepts",
            "pdf": "https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/"},

        4: {"title": "Database System Concepts - Korth",
            "pdf": "https://www.db-book.com/slides-dir/"},

        5: {"title": "Let Us C - Kanetkar",
            "pdf": "https://archive.org/details/letusC"},

        6: {"title": "Python Crash Course",
            "pdf": "https://ehmatthes.github.io/pcc_2e/"}
    }

    if book_id not in BOOKS:
        return "Book Not Found", 404

    return render_template("read_book.html", book=BOOKS[book_id])


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True)
