from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import sqlite3

DB_NAME = "users.db"

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    user_id, name, password_hash = row

    # password match check
    if not check_password_hash(password_hash, password):
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    # login success
    session["user_id"] = user_id
    session["username"] = name
    return jsonify({"success": True, "message": "Login successful"})
