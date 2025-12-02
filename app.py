from flask import Flask, render_template, request, jsonify, abort
import requests

app = Flask(__name__)

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"


@app.route("/")
def home():
    # Main dashboard page
    return render_template("dashboard.html")


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
        # description thoda short kar dete hain
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
    Reading mode page for one book.
    Hum yahan se bhi Google Books API se detail laayenge.
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


if __name__ == "__main__":
    app.run(debug=True)
