# Python Projects 🙌

This repository contains multiple Python projects demonstrating different concepts and techniques.

## Projects

1. **[NLP-Text-to-SQL](#nlp-text-to-sql)** - Convert natural language to SQL queries
2. **[Bulletproof Scraper](#bulletproof-scraper)** - Web scraping with automated testing

---

## NLP-Text-to-SQL

💻 Convert plain English questions into SQL queries and run them instantly on a SQLite database.

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup and Installation

1. **Navigate to the project directory:**
   ```bash
   cd NLP-Text-to-SQL
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Linux/Mac:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create and seed the database:**
   ```bash
   python scripts/create_db.py --db books.db
   ```

### How to Run

**Start the Streamlit application:**
```bash
streamlit run app/app.py --server.port 8501
```

The app will open in your browser at `http://localhost:8501`

### Example Queries
- "Show me titles and price of fantasy books under $20"
- "List books by J.K. Rowling"
- "How many books published after 2010?"
- "Top 5 most expensive books"

For more details, see the [NLP-Text-to-SQL README](NLP-Text-to-SQL/README.md)

---

## Bulletproof Scraper

🛡️ A self-validating web scraper that automatically tests scraped data for quality issues.

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (to scrape http://books.toscrape.com)

### Setup and Installation

1. **Navigate to the project directory:**
   ```bash
   cd bulletproof_scraper
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Linux/Mac:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### How to Run

**Run the scraper:**
```bash
python scraper.py
```

This will scrape book data from http://books.toscrape.com and save it to `books.csv`

**Run the tests:**
```bash
pytest test_scraper.py -v
```

The tests validate:
- Data structure and format
- Price formatting
- Required fields presence
- Data quality

For more details, see the [Bulletproof Scraper README](bulletproof_scraper/readme)

---

## General Notes

- Each project should be run in its own virtual environment to avoid dependency conflicts
- Make sure to activate the virtual environment before running any commands
- All commands should be run from the respective project directory

## Contributing

Feel free to contribute to any of these projects by opening issues or pull requests!
