from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "librarysecret"

# ---------------- DB ----------------
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    db.commit()
    db.close()

init_db()

# --------------- BOOK DATA ----------------
BOOKS = [
    {"id": 1, "title": "Operating System Concepts", "author": "Silberschatz"},
    {"id": 2, "title": "Computer Networks", "author": "Tanenbaum"},
    {"id": 3, "title": "Database System Concepts", "author": "Korth"},
    {"id": 4, "title": "Artificial Intelligence", "author": "Russell"},
    {"id": 5, "title": "Data Structures Using C", "author": "Tenenbaum"},
    {"id": 6, "title": "Python Programming", "author": "Guido"},
    {"id": 7, "title": "Machine Learning", "author": "Tom Mitchell"},
    {"id": 8, "title": "Compiler Design", "author": "Aho"},
    {"id": 9, "title": "Web Development", "author": "MDN"},
    {"id": 10, "title": "Software Engineering", "author": "Pressman"},
]

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect("/login")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?",
                          (email, password)).fetchone()
        db.close()

        if user:
            session["user"] = email
            return redirect("/dashboard")
        else:
            return "Invalid login details"

    return render_template("login.html")

# -------- SIGNUP --------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            db = get_db()
            db.execute("INSERT INTO users (email,password) VALUES(?,?)",
                       (email, password))
            db.commit()
            db.close()
            return redirect("/login")
        except:
            return "User already exists"

    return render_template("signup.html")

# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------- SEARCH API --------
@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").lower()
    result = []
    for book in BOOKS:
        if query in book["title"].lower() or query in book["author"].lower():
            result.append(book)
    return jsonify(result)

# -------- READ BOOK PAGE --------
@app.route("/read-book/<int:bid>")
def read_book(bid):
    book = next((b for b in BOOKS if b["id"] == bid), None)
    if not book:
        return "Book not found"
    return f"""
    <h1>{book['title']}</h1>
    <p>By {book['author']}</p>
    <p>Reading Mode (Demo Page)</p>
    <a href='/dashboard'>Back</a>
    """

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
