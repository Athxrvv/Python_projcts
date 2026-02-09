import re
from typing import Tuple

# Lightweight rule-based NL -> SQL mapper for the "books" table.
COLUMNS = {
    "title": "title",
    "titles": "title",
    "author": "author",
    "authors": "author",
    "price": "price",
    "year": "year",
    "genre": "genre",
    "stock": "stock",
    "all": "*",
    "everything": "*",
}

def parse_columns(text: str) -> str:
    cols = []
    for key, col in COLUMNS.items():
        if re.search(r"\b" + re.escape(key) + r"\b", text):
            if col == "*":
                return "*"
            cols.append(col)
    if cols:
        seen = []
        for c in cols:
            if c not in seen:
                seen.append(c)
        return ", ".join(seen)
    return "title, author, price, year"

def quote_sql_value(val: str) -> str:
    val = val.strip()
    if re.fullmatch(r"\d+(\.\d+)?", val):
        return val
    return "'" + val.replace("'", "''") + "'"

def extract_author(text: str):
    m = re.search(r"\bby\s+([A-Za-z0-9 .'-]+)", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"author\s+([A-Za-z0-9 .'-]+)", text, flags=re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return None

def extract_genre(text: str):
    m = re.search(r"\bgenre\s+([A-Za-z0-9 &'-]+)", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"\b(in|of)\s+([A-Za-z0-9 &'-]+)\s+(books|novels|titles)?", text, flags=re.IGNORECASE)
    if m2:
        return m2.group(2).strip()
    return None

def extract_price_filter(text: str):
    m = re.search(r"(under|less than|below)\s+\$?(\d+(\.\d+)?)", text)
    if m:
        return ("<", float(m.group(2)))
    m = re.search(r"(over|more than|above)\s+\$?(\d+(\.\d+)?)", text)
    if m:
        return (">", float(m.group(2)))
    m = re.search(r"between\s+\$?(\d+(\.\d+)?)\s+and\s+\$?(\d+(\.\d+)?)", text)
    if m:
        return ("between", (float(m.group(1)), float(m.group(3))))
    return None

def extract_year_filter(text: str):
    m = re.search(r"(after|since)\s+(\d{4})", text)
    if m:
        return (">", int(m.group(2)))
    m = re.search(r"(before|earlier than)\s+(\d{4})", text)
    if m:
        return ("<", int(m.group(2)))
    m = re.search(r"between\s+(\d{4})\s+and\s+(\d{4})", text)
    if m:
        return ("between", (int(m.group(1)), int(m.group(2))))
    m2 = re.search(r"\b(19|20)\d{2}\b", text)
    if m2:
        return ("=", int(m2.group(0)))
    return None

def nl_to_sql(nl: str) -> Tuple[str, str]:
    text = nl.lower()
    cols = parse_columns(text)
    where_clauses = []

    author = extract_author(nl)
    if author:
        where_clauses.append(f"author LIKE {quote_sql_value('%' + author + '%')}")

    genre = extract_genre(nl)
    if genre:
        where_clauses.append(f"genre LIKE {quote_sql_value('%' + genre + '%')}")

    pfilter = extract_price_filter(text)
    if pfilter:
        if pfilter[0] == "between":
            a, b = pfilter[1]
            where_clauses.append(f"price BETWEEN {a} AND {b}")
        else:
            op, v = pfilter
            where_clauses.append(f"price {op} {v}")

    yfilter = extract_year_filter(text)
    if yfilter:
        if yfilter[0] == "between":
            a, b = yfilter[1]
            where_clauses.append(f"year BETWEEN {a} AND {b}")
        else:
            op, v = yfilter
            where_clauses.append(f"year {op} {v}")

    if re.search(r"\bhow many\b|\bcount\b|\bnumber of\b", text):
        select_clause = "COUNT(*) as count"
    elif cols.strip() == "*":
        select_clause = "*"
    else:
        select_clause = cols

    sql = f"SELECT {select_clause} FROM books"

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    top_n = None
    m = re.search(r"top\s+(\d+)", text)
    if m:
        top_n = int(m.group(1))
    if re.search(r"most expensive|expensive|highest price", text):
        sql += " ORDER BY price DESC"
        if top_n:
            sql += f" LIMIT {top_n}"
    elif re.search(r"cheapest|least expensive|lowest price", text):
        sql += " ORDER BY price ASC"
        if top_n:
            sql += f" LIMIT {top_n}"
    else:
        m2 = re.search(r"\bshow\s+(\d+)\b|\blist\s+(\d+)\b", text)
        if m2:
            n = int([g for g in m2.groups() if g][0])
            sql += f" LIMIT {n}"

    if "limit" not in sql.lower() and "count(" not in select_clause.lower():
        sql += " LIMIT 50"

    return sql, select_clause