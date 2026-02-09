import re
import requests
from scraper import scrape_books

books = scrape_books(1)  # test on 1 page for speed

def test_books_exist():
    assert len(books) > 0, "No books found! Structure may have changed."

def test_price_format():
    for book in books:
        assert re.match(r"£\d+\.\d{2}", book["price"]), f"Bad price: {book['price']}"

def test_image_url_valid():
    for book in books[:5]:  # limit requests
        response = requests.get(book["image_url"])
        assert response.status_code == 200, f"Broken image: {book['image_url']}"

def test_title_not_empty():
    for book in books:
        assert book["title"].strip() != "", "Empty title detected!"
