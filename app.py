from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"   # koi bhi random string

# ----------------- DATABASE SETUP -----------------
BASE_DIR = os.path.abspath(os.path.dirname(_file_))
DB_PATH = os.path.join(BASE_DIR, "users.db")


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

# ----------------- SIMPLE PAGES -----------------


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    # tumhari login.html UI yahin use hogi
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    # tumhari signup.html UI yahin use hogi
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("dashboard.html", username=session.get("username"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ----------------- SIGNUP API (JSON) -----------------
# yeh tumhare JS wale  fetch("/api/signup")  ke liye hai
@app.route("/api/signup", methods=["POST"])
def api_signup():
    try:
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not name or not email or not password:
            return jsonify({"success": False, "message": "Please fill all fields."}), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (?,?,?)",
            (name, email, password),
        )
        conn.commit()
        conn.close()

        return jsonify(
            {"success": True, "message": "Signup successful. Please login."}
        )
    except sqlite3.IntegrityError:
        # email duplicate
        return jsonify(
            {"success": False, "message": "This email is already registered."}
        ), 400
    except Exception as e:
        # koi bhi aur error -> JS me "Something went wrong" ki jagah proper message
        return jsonify({"success": False, "message": f"Server error: {e}"}), 500


# ----------------- LOGIN API (JSON) -----------------
# yeh tumhare JS wale  fetch("/api/login")  ke liye hai
@app.route("/api/login", methods=["POST"])
def api_login():
    try:
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return jsonify(
                {"success": False, "message": "Enter email and password."}
            ), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, password FROM users WHERE email = ?", (email,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return jsonify(
                {"success": False, "message": "Invalid email or password."}
            ), 401

        user_id, name, stored_password = row

        if stored_password != password:
            return jsonify(
                {"success": False, "message": "Invalid email or password."}
            ), 401

        # login success
        session["user_id"] = user_id
        session["username"] = name
        return jsonify({"success": True, "message": "Login successful."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {e}"}), 500


# ----------------- BOOK SEARCH API -----------------
BOOKS = [
    {"id": 1, "title": "Operating System Concepts", "author": "Silberschatz"},
    {"id": 2, "title": "Computer Networks", "author": "Tanenbaum"},
    {"id": 3, "title": "Database System Concepts", "author": "Korth"},
    {"id": 4, "title": "Artificial Intelligence", "author": "Russell"},
    {"id": 5, "title": "Data Structures Using C", "author": "Tenenbaum"},
    {"id": 6, "title": "Python Programming", "author": "Guido van Rossum"},
    {"id": 7, "title": "Machine Learning", "author": "Tom Mitchell"},
    {"id": 8, "title": "Compiler Design", "author": "Alfred V. Aho"},
    {"id": 9, "title": "Web Development", "author": "MDN"},
    {"id": 10, "title": "Software Engineering", "author": "Pressman"},
]


@app.route("/api/search")
def api_search():
    q = (request.args.get("q") or "").lower()
    results = []
    for b in BOOKS:
        if q in b["title"].lower() or q in b["author"].lower():
            results.append(b)
    return jsonify(results)


# OPTIONAL: read-book page agar tum "Read" button se open kara rahe ho
@app.route("/read-book/<int:book_id>")
def read_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return "Book not found"
    return f"""
    <h1>{book['title']}</h1>
    <p>by {book['author']}</p>
    <p>Reading mode page (demo).</p>
    <a href="{url_for('dashboard')}">Back to dashboard</a>
    """


# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app.run(debug=True)
