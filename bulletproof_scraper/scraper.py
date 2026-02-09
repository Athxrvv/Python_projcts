import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape_books(pages=3):
    books = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select("article.product_pod"):
            title = book.h3.a["title"]
            traw_price = book.select_one(".price_color").text.strip()
            price = traw_price.encode("latin1").decode("utf-8")

            image_rel = book.img["src"]
            image_url = urljoin(url, image_rel)

            books.append({
                "title": title,
                "price": price,
                "image_url": image_url
            })

    return books


def save_to_csv(data, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    books = scrape_books()
    save_to_csv(books)
    print("Scraping completed and saved to CSV.")
