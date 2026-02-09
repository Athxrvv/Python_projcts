import sqlite3
import pandas as pd
from typing import Any
from pathlib import Path

def execute_sql(db_path: str, sql: str) -> pd.DataFrame:
    db_file = Path(db_path)
    if not db_file.exists():
        raise FileNotFoundError(f"Database file '{db_path}' not found.")
    conn = sqlite3.connect(str(db_file))
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df