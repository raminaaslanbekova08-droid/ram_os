import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"
QUERIES_PATH = Path(__file__).resolve().parent.parent / "queries" / "04_check_queries.sql"

def run_queries():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        sql_text = f.read()

    statements = [s.strip() for s in sql_text.split(";") if s.strip()]

    for i, stmt in enumerate(statements, 1):
        print(f"\n--- ЗАПРОС {i} ---")
        print(stmt + ";")
        try:
            cur.execute(stmt)
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(" | ".join(str(val) for val in row))
            else:
                print("(пусто)")
        except sqlite3.Error as e:
            print(f"[ОШИБКА SQL] {e}")

    conn.close()

if __name__ == "__main__":
    run_queries()