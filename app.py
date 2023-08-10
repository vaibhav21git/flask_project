from flask import Flask, render_template, request, redirect

import sqlite3


app = Flask(__name__)


# Configure SQLite database

DATABASE = "books.db"


def create_table():
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)"
    )

    conn.commit()

    conn.close()


@app.route("/")
def index():
    create_table()

    conn = sqlite3.connect(DATABASE)

    books = conn.execute("SELECT * FROM books").fetchall()

    conn.close()

    return render_template("index.html", books=books)


@app.route("/add_book", methods=["POST"])
def add_book():
    title = request.form.get("title")

    if title:
        conn = sqlite3.connect(DATABASE)

        conn.execute("INSERT INTO books (title) VALUES (?)", (title,))

        conn.commit()

        conn.close()

    return redirect("/")


@app.route("/delete_book/<int:id>")
def delete_book(id):
    conn = sqlite3.connect(DATABASE)

    conn.execute("DELETE FROM books WHERE  id = ?", (id,))

    conn.commit()

    conn.close()

    return redirect("/")


@app.route("/update_book/<int:id>", methods=["GET", "POST"])
def update_book(id):
    conn = sqlite3.connect(DATABASE)

    if request.method == "POST":
        new_title = request.form.get("new_title")

        if new_title:
            conn.execute("UPDATE books SET title = ? WHERE id = ?", (new_title, id))

            conn.commit()

    book = conn.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()

    conn.close()

    return render_template("update_book.html", book=book)


if __name__ == "__main__":
    app.run(port=5003, debug=True)


# hello this is comment
