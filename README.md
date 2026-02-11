# Python Projects Collection 🐍

This repository contains multiple Python projects showcasing different technologies and techniques.

## 📋 Prerequisites

Before running any project, ensure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- Internet connection (for package installation and web scraping)

### Check Python Version
```bash
python --version
# or
python3 --version
```

---

## 🚀 Projects in This Repository

### 1. 💻 NLP Text-to-SQL
Convert plain English questions into SQL queries and run them instantly on a SQLite database.

**Location:** `NLP-Text-to-SQL/`

**Technologies:** Streamlit, Pandas, SQLite

#### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd NLP-Text-to-SQL
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create and seed the database:**
   ```bash
   python scripts/create_db.py --db books.db
   ```

6. **Run the Streamlit app:**
   ```bash
   streamlit run app/app.py --server.port 8501
   ```

7. **Access the app:**
   - Open your browser and go to: `http://localhost:8501`

8. **Try example queries:**
   - "Show me titles and price of fantasy books under $20"
   - "How many books by George Orwell?"
   - "Show the most expensive books"

---

### 2. 🛡️ Bulletproof Web Scraper
A self-validating web scraper with automated testing that scrapes book data from a demo e-commerce site.

**Location:** `bulletproof_scraper/`

**Technologies:** Requests, BeautifulSoup4, Pytest

#### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd bulletproof_scraper
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the scraper:**
   ```bash
   python scraper.py
   ```
   This will scrape book data and save it to `books.csv`
   
   **Note:** Internet connection required to access http://books.toscrape.com/

6. **Run tests:**
   ```bash
   pytest test_scraper.py -v
   ```
   This runs automated tests to verify the scraper works correctly

7. **View the scraped data:**
   ```bash
   cat books.csv
   ```
   Or open `books.csv` in a spreadsheet application

---

## 🔧 Common Issues and Solutions

### Issue: "python: command not found"
**Solution:** Try using `python3` instead of `python`

### Issue: "pip: command not found"
**Solution:** Try using `pip3` instead of `pip`, or install pip:
```bash
python -m ensurepip --upgrade
```

### Issue: Virtual environment activation fails
**Solution:** 
- Make sure you're in the correct project directory
- On Windows, you may need to enable script execution:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Issue: "Module not found" errors
**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 📚 Learning Resources

- **Python Official Docs:** https://docs.python.org/3/
- **Streamlit Docs:** https://docs.streamlit.io/
- **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Pytest Docs:** https://docs.pytest.org/

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements!

---

## 📝 Notes

- Each project has its own virtual environment to keep dependencies isolated
- Always activate the virtual environment before running a project
- For detailed project-specific information, see the README files in each project directory
