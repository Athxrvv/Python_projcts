-- Simple bookstore schema
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    price REAL,
    year INTEGER,
    stock INTEGER
);