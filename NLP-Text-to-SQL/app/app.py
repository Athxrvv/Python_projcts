import streamlit as st
from src.nl2sql_rulebased import nl_to_sql
from src.db_utils import execute_sql
import os

DEFAULT_DB = "books.db"

st.set_page_config(page_title="Text-to-SQL Demo", layout="wide")
st.title("Text-to-SQL — Toy Bookstore")

db_path = st.sidebar.text_input("SQLite DB path", value=DEFAULT_DB)
if not os.path.exists(db_path):
    st.sidebar.warning(f"Database file '{db_path}' not found. Run scripts/create_db.py to create it.")
query = st.text_area("Enter a natural language query about the books database", height=120,
                     value="Show me titles and price of fantasy books under $20.")

if st.button("Generate SQL and Run"):
    sql, select_clause = nl_to_sql(query)
    st.subheader("Generated SQL")
    st.code(sql)
    try:
        df = execute_sql(db_path, sql)
        st.subheader("Results")
        st.dataframe(df)
        st.write(f"Rows: {len(df)}")
    except Exception as e:
        st.error(f"Error executing SQL: {e}")

st.markdown("### Example queries")
st.write(
    """
- Show me titles and price of fantasy books under $20.
- List books by J.K. Rowling.
- How many books published after 2010?
- Top 5 most expensive books.
- Find all books by 'George Orwell' in 1949.
"""
)