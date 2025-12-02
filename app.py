from flask import (
    Flask, render_template, request,
    jsonify, session, redirect, url_for, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(_name_)
app.secret_key = "change-this-secret-key"  # koi random string rakh lena

DB_NAME = "users.db"

# ---------- USER DB SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- DEMO BOOK DATA ----------
BOOKS = {
    1: {
        "id": 1,
        "title": "Introduction to Algorithms",
        "author": "Cormen, Leiserson, Rivest, Stein",
        "category": "computer science",
        "description": "Classic algorithms book covering sorting, searching, dynamic programming and graph algorithms.",
        "chapters": [
            {"number": 1, "title": "Foundations", "content": "Basic concepts, asymptotic notation, algorithm analysis."},
            {"number": 2, "title": "Sorting and Order Statistics", "content": "Insertion sort, merge sort, heapsort, quicksort."},
            {"number": 3, "title": "Data Structures", "content": "Stacks, queues, linked lists, trees and hash tables."}
        ]
    },
    2: {
        "id": 2,
        "title": "Operating System Concepts",
        "author": "Silberschatz, Galvin, Gagne",
        "category": "computer science",
        "description": "Fundamentals of processes, threads, scheduling, memory management and file systems.",
        "chapters": [
            {"number": 1, "title": "Introduction to Operating Systems", "content": "What an OS does, types of OS and structure."},
            {"number": 2, "title": "Processes", "content": "Process states, PCB, context switching and scheduling."},
            {"number": 3, "title": "Memory Management", "content": "Paging, segmentation, virtual memory and page replacement."}
        ]
    },
    3: {
        "id": 3,
        "title": "Computer Networks",
        "author": "Kurose & Ross",
        "category": "computer science",
        "description": "Layered view of networking: application, transport, network and link layers.",
        "chapters": [
            {"number": 1, "title": "Introduction", "content": "Network edges, core, delay, loss and Internet structure."},
            {"number": 2, "title": "Application Layer", "content": "Web, HTTP, DNS, client-server and P2P."},
            {"number": 3, "title": "Transport Layer", "content": "UDP, TCP, reliability and congestion control."}
        ]
    },
    4: {
        "id": 4,
        "title": "Database System Concepts",
        "author": "Silberschatz, Korth, Sudarshan",
        "category": "computer science",
        "description": "Relational model, SQL, normalization, transactions and recovery.",
        "chapters": [
            {"number": 1, "title": "Introduction to Databases", "content": "What is a DBMS, advantages, architecture."},
            {"number": 2, "title": "Relational Model", "content": "Relations, keys, constraints, relational algebra."},
            {"number": 3, "title": "SQL", "content": "Basic queries, joins, subqueries and views."}
        ]
    },
}


# ---------- AUTH PAGES ----------
@app.route("/")
def root():
    # agar login hai to dashboard, nahi to login
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("dashboard.html", user_name=session.get("user_name"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ---------- AUTH APIs ----------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"ok": False, "message": "All fields are required."}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?,?,?)",
            (name, email, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "message": "Email already registered."}), 400

    return jsonify({"ok": True, "message": "Signup successful. Please login."})


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"ok": False, "message": "Email and password are required."}), 400

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, password_hash FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"ok": False, "message": "Invalid email or password."}), 401

    user_id, name, pwd_hash = row

    if not check_password_hash(pwd_hash, password):
        return jsonify({"ok": False, "message": "Invalid email or password."}), 401

    # success
    session["user_id"] = user_id
    session["user_name"] = name
    return jsonify({"ok": True, "message": "Login successful."})


# ---------- BOOK SEARCH + READER ----------
@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip().lower()
    results = []

    for b in BOOKS.values():
        if b.get("category", "").lower() != "computer science":
            continue

        if q == "":
            results.append({"id": b["id"], "title": b["title"], "author": b["author"]})
        else:
            text = (b["title"] + " " + b["author"] + " " + b["description"]).lower()
            if q in text:
                results.append({"id": b["id"], "title": b["title"], "author": b["author"]})

    return jsonify(results)


@app.route("/read-book/<int:book_id>")
def read_book(book_id):
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    book = BOOKS.get(book_id)
    if not book:
        abort(404)
    return render_template("read_book.html", book=book)


if _name_ == "_main_":
    app.run(debug=True)
