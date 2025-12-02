from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# ---------------- DEMO COMPUTER SCIENCE BOOKS ----------------
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
            {"number": 1, "title": "Introduction to Operating Systems", "content": "What an OS does, different types of operating systems."},
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
            {"number": 1, "title": "Computer Networks and the Internet", "content": "Network edges, core, delay and loss."},
            {"number": 2, "title": "Application Layer", "content": "Web, HTTP, DNS, client-server and P2P models."},
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
            {"number": 1, "title": "Introduction to Databases", "content": "What is a DBMS, advantages and architecture."},
            {"number": 2, "title": "Relational Model", "content": "Relations, keys, constraints and relational algebra."},
            {"number": 3, "title": "SQL", "content": "Basic queries, joins, subqueries and views."}
        ]
    },
}
# ---------------------------------------------------------------


@app.route("/")
def home():
    # seedha dashboard kholega
    return render_template("dashboard.html")


@app.route("/api/search")
def api_search():
    """
    Search Computer Science books.
    - If q empty: return all CS books
    - Else filter by title/author/description
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
                "author": b["author"],
            })
        else:
            blob = (b["title"] + " " + b["author"] + " " + b["description"]).lower()
            if q in blob:
                results.append({
                    "id": b["id"],
                    "title": b["title"],
                    "author": b["author"],
                })

    return jsonify(results)


@app.route("/read-book/<int:book_id>")
def read_book(book_id):
    """
    Reading mode page for a single book.
    """
    book = BOOKS.get(book_id)
    if not book:
        return abort(404)
    return render_template("read_book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
