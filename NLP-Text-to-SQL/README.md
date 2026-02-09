```markdown
💻 Text-to-SQL 
Convert plain English questions into SQL queries and run them instantly on a SQLite database.
Built with Streamlit, OpenAI GPT API, and SQLite.

Simple Text-to-SQL demo for a toy "books" database.

Quick setup
1. Create virtual env and install deps:
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

2. Create & seed the DB:
   python scripts/create_db.py --db books.db

3. Run the Streamlit app:
   streamlit run app/app.py --server.port 8501

Project layout
- schema/            SQL schema files
- scripts/           utilities (create DB)
- src/               Python package: nl2sql mapper and DB utils
- app/               Streamlit app
- examples/          example NL queries

Next improvements
- Add fuzzy/entity matching (spaCy or Sentence-BERT)
- Generate synthetic NL→SQL pairs and fine-tune T5/BART
- Add tests / CI / deploy to Streamlit Cloud
```
