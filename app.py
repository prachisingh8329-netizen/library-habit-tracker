from flask import Flask, render_template, request, jsonify, abort

app = Flask(_name_)

# --------- DEMO COMPUTER SCIENCE BOOK DATA ----------
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
            {"number": 1, "title": "Introduction to Operating Systems", "content": "What an OS does, types of OS and overall structure."},
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
            {"number": 1, "title": "Computer Networks and the Internet", "content": "Network edges, core, delay, loss and Internet structure."},
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
            {"number": 1, "title": "Introduction to Databases", "content": "What is a DBMS, its advantages and architecture."},
            {"number": 2, "title": "Relational Model", "content": "Relations, keys, constraints, relational algebra."},
            {"number": 3, "title": "SQL", "content": "Basic queries, joins, subqueries and views."}
        ]
    },
}
# ----------------------------------------------------


@app.route("/")
def home():
    # by default dashboard hi khulega
    return render_template("dashboard.html")


@app.route("/api/search")
def api_search():
    """
    Frontend se: /api/search?q=...
    Sirf Computer Science category ki books return hogi.
    Agar q empty hai -> saari CS books.
    Agar q diya hai -> title/author/description me match karega.
    """
    q = request.args.get("q", "").strip().lower()

    results = []
    for b in BOOKS.values():
        if b.get("category", "").lower() != "computer science":
            continue

        if q == "":
            results.append({
                "id": b["id"],
                "title": b["title"],
                "author": b["author"]
            })
        else:
            text = (b["title"] + " " + b["author"] + " " + b["description"]).lower()
            if q in text:
                results.append({
                    "id": b["id"],
                    "title": b["title"],
                    "author": b["author"]
                })

    return jsonify(results)


@app.route("/read-book/<int:book_id>")
def read_book(book_id):
    """Reading mode page for a specific book."""
    book = BOOKS.get(book_id)
    if not book:
        return abort(404)
    return render_template("read_book.html", book=book)


if _name_ == "_main_":
    app.run(debug=True)
