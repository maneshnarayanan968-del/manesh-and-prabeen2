"""A small SQL-backed book catalogue using Python's built-in SQLite support."""
import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "books.db"


def connect(db_path=DEFAULT_DB):
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(db_path=DEFAULT_DB):
    with connect(db_path) as conn:
        conn.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        conn.executescript((ROOT / "seed.sql").read_text(encoding="utf-8"))


def list_books(db_path=DEFAULT_DB):
    with connect(db_path) as conn:
        return conn.execute(
            "SELECT id, title, author, genre, published_year, isbn "
            "FROM books ORDER BY title"
        ).fetchall()


def search_books(term, db_path=DEFAULT_DB):
    """Search title, author, or genre using bound parameters."""
    pattern = f"%{term}%"
    with connect(db_path) as conn:
        return conn.execute(
            """SELECT id, title, author, genre, published_year, isbn
               FROM books
               WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
               ORDER BY title""",
            (pattern, pattern, pattern),
        ).fetchall()


def add_book(title, author, genre, published_year=None, isbn=None, db_path=DEFAULT_DB):
    with connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO books (title, author, genre, published_year, isbn)
               VALUES (?, ?, ?, ?, ?)""",
            (title, author, genre, published_year, isbn),
        )
        return cursor.lastrowid


def print_books(rows):
    if not rows:
        print("No books found.")
        return
    for row in rows:
        print(f"[{row['id']}] {row['title']} — {row['author']} "
              f"({row['published_year'] or 'year unknown'}) | {row['genre']}")


def main():
    parser = argparse.ArgumentParser(description="SQL Book Finder")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite database file path")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create tables and load sample data")
    sub.add_parser("list", help="List all books")
    search = sub.add_parser("search", help="Search title, author, or genre")
    search.add_argument("term")

    add = sub.add_parser("add", help="Add a book")
    add.add_argument("--title", required=True)
    add.add_argument("--author", required=True)
    add.add_argument("--genre", required=True)
    add.add_argument("--year", type=int)
    add.add_argument("--isbn")

    args = parser.parse_args()
    db_path = args.db

    if args.command == "init":
        initialize(db_path)
        print(f"Database initialized: {db_path}")
    elif args.command == "list":
        print_books(list_books(db_path))
    elif args.command == "search":
        print_books(search_books(args.term, db_path))
    elif args.command == "add":
        new_id = add_book(args.title, args.author, args.genre, args.year, args.isbn, db_path)
        print(f"Book added with ID {new_id}")


if __name__ == "__main__":
    main()
