# SQL Book Finder

A small SQL-backed book catalogue built with Python and SQLite. It demonstrates schema creation, seed data, parameterized SQL queries, a command-line interface, and automated tests.

## Features

- `schema.sql`: `books` table, constraints, and indexes
- `seed.sql`: sample book records
- `app.py`: initialize, list, search, and add books
- Parameterized queries (`?` placeholders) for user-supplied values
- Unit tests using Python's built-in `unittest`
- No third-party packages required

## Requirements

- Python 3.9 or newer recommended
- SQLite is included with standard Python builds

## Run quickly

Unzip the project and open a terminal in the project directory.

```bash
python app.py init
python app.py list
python app.py search "Clean Code"
python app.py search Databases
python -m unittest discover -s tests -v
```

On some systems, use `python3` instead of `python`.

## Sample queries

The project uses parameterized SQL in `app.py`. Examples of the underlying SQL:

```sql
-- Search across title, author, and genre
SELECT id, title, author, genre, published_year, isbn
FROM books
WHERE title LIKE ?
   OR author LIKE ?
   OR genre LIKE ?
ORDER BY title;

-- List books in alphabetical order
SELECT id, title, author, genre, published_year, isbn
FROM books
ORDER BY title;

-- Insert a new book
INSERT INTO books (title, author, genre, published_year, isbn)
VALUES (?, ?, ?, ?, ?);
```

The `?` placeholders bind values separately from SQL code, helping protect against SQL injection.

## Add a book

```bash
python app.py add --title "SQL Basics" --author "A. Writer" --genre "Databases" --year 2024 --isbn "9780000000000"
```

Then list or search to see the new record:

```bash
python app.py list
python app.py search "SQL Basics"
```

ISBN values must be unique.

## Files

```text
sql-book-finder/
├── app.py
├── schema.sql
├── seed.sql
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── tests/
    └── test_app.py
```

## Database location

By default, the database is created as `books.db` in the project directory. You can select another SQLite file with `--db`:

```bash
python app.py --db ./demo.db init
python app.py --db ./demo.db list
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Publish to GitHub

1. Create a new empty repository on GitHub.
2. Extract this ZIP and open a terminal in the extracted folder.
3. Run:

```bash
git init
git add .
git commit -m "Add SQL Book Finder project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example repository URL with your own. This ZIP is a project package; it has not been published to GitHub automatically.
