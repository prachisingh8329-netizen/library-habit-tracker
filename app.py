from flask import Flask, render_template, request, jsonify, abort
import sqlite3
import os
import requests

app = Flask(__name__)

# -------------- CONFIG --------------
DB_PATH = "users.db"
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"
# ------------------------------------


# -------------- DB HELPER --------------
def init_db():
    """Create users table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect(DB_PATH)


# initialize on startup
if not os.path.exists(DB_PATH):
    init_db()
# ---------------------------------------


# -------------- PAGE ROUTES --------------

@app.route("/")
def landing_page():
    """
    Get Started / home page.
    Make sure you have templates/index.html
    """
    return render_template("index.html")


@app.route("/signup")
def signup_page():
    """
    Signup UI page.
    templates/signup.html (your nice glassmorphism signup)
    """
    return render_template("signup.html")


@app.route("/login")
def login_page():
    """
    Login UI page.
    templates/login.html
    """
    return render_template("login.html")


@app.route("/dashboard")
def dashboard_page():
    """
    Main dashboard UI page.
    templates/dashboard.html (the big tracker you and I made)
    """
    return render_template("dashboard.html")


# -------------- AUTH APIs --------------

@app.route("/api/signup", methods=["POST"])
def api_signup():
    """
    Frontend se expected JSON:
    { "name": "...", "email": "...", "password": "..." }
    """
    data = request.get_json(force=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        # email already exists
        return jsonify({"success": False, "message": "Email already registered."}), 409
    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"success": False, "message": "Server error."}), 500

    return jsonify({"success": True, "message": "Signup successful!"})


@app.route("/api/login", methods=["POST"])
def api_login():
    """
    Frontend se expected JSON:
    { "email": "...", "password": "..." }
    """
    data = request.get_json(force=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required."}), 400

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM users WHERE email = ? AND password = ?",
            (email, password),
        )
        row = c.fetchone()
        conn.close()
    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"success": False, "message": "Server error."}), 500

    if not row:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    # Simple response: frontend redirect karega /dashboard pe
    return jsonify({"success": True, "message": "Login successful!", "redirect": "/dashboard"})


# -------------- ONLINE BOOK SEARCH (GOOGLE BOOKS) --------------

@app.route("/api/search")
def api_search():
    """
    Online search:
    - User jo bhi type karega (q), usko Google Books pe bhejenge
    - Sirf computer science related results try karenge
    - Return: id, title, author, description ka short part, preview_link
    """
    q = request.args.get("q", "").strip()
    if not q:
        # agar blank hai to default CS query
        q = "computer science"

    params = {
        "q": q + " subject:computer science",
        "maxResults": 20,
        "printType": "books",
    }

    try:
        r = requests.get(GOOGLE_BOOKS_API, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print("Google Books error:", e)
        return jsonify([])

    results = []
    for item in data.get("items", []):
        volume_id = item.get("id")
        info = item.get("volumeInfo", {}) or {}
        title = info.get("title", "Untitled")
        authors = ", ".join(info.get("authors", []))
        desc = info.get("description", "") or ""
        if len(desc) > 220:
            desc = desc[:220] + "..."

        preview = info.get("previewLink", "")

        results.append({
            "id": volume_id,
            "title": title,
            "author": authors,
            "description": desc,
            "preview_link": preview
        })

    return jsonify(results)


@app.route("/read-book/<volume_id>")
def read_book(volume_id):
    """
    Reading mode page for one online book (Google Books).
    """
    try:
        r = requests.get(f"{GOOGLE_BOOKS_API}/{volume_id}", timeout=10)
        if r.status_code != 200:
            return abort(404)
        item = r.json()
    except Exception as e:
        print("detail error:", e)
        return abort(404)

    info = item.get("volumeInfo", {}) or {}

    book = {
        "id": volume_id,
        "title": info.get("title", "Untitled"),
        "author": ", ".join(info.get("authors", [])),
        "description": info.get("description", ""),
        "page_count": info.get("pageCount"),
        "publisher": info.get("publisher"),
        "published_date": info.get("publishedDate"),
        "categories": ", ".join(info.get("categories", [])),
        "preview_link": info.get("previewLink", "")
    }

    return render_template("read_book.html", book=book)


# ---------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
