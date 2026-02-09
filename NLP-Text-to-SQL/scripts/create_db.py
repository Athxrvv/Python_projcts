#!/usr/bin/env python3
import sqlite3
import argparse
import os
from pathlib import Path

SAMPLE_DATA = [
    ("1984", "George Orwell", "Dystopian", 9.99, 1949, 12),
    ("Animal Farm", "George Orwell", "Political Satire", 7.99, 1945, 8),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 12.99, 1997, 30),
    ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fantasy", 12.99, 1998, 25),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 14.99, 1937, 18),
    ("A Game of Thrones", "George R.R. Martin", "Fantasy", 22.50, 1996, 5),
    ("Clean Code", "Robert C. Martin", "Programming", 31.50, 2008, 4),
    ("The Pragmatic Programmer", "Andrew Hunt", "Programming", 28.00, 1999, 6),
    ("Sapiens", "Yuval Noah Harari", "History", 19.99, 2011, 10),
    ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 8.99, 1951, 7),
]

def create_db(db_path: str):
    db_path = Path(db_path)
    if db_path.exists():
        print(f"Overwriting existing database at {db_path}")
        db_path.unlink()
    conn = sqlite3.connect(str(db_path))
    schema_path = Path(__file__).resolve().parents[1] / "schema" / "schema.sql"
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO books (title, author, genre, price, year, stock) VALUES (?, ?, ?, ?, ?, ?)",
        SAMPLE_DATA,
    )
    conn.commit()
    conn.close()
    print(f"Created and seeded database at {db_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="books.db", help="Path to sqlite db file")
    args = parser.parse_args()
    create_db(args.db)