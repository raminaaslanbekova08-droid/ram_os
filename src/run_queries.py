import sqlite3
from app_functions import register_all_functions, DB_PATH

conn = sqlite3.connect(DB_PATH)
register_all_functions(conn)
cur = conn.cursor()

with open("queries/10_advanced_queries.sql", encoding="utf-8") as f:
    sql = f.read()

statements = [s.strip() for s in sql.split(";") if s.strip()]

for i, stmt in enumerate(statements, 1):
    print(f"\n--- Запрос {i} ---")
    try:
        cur.execute(stmt)
        rows = cur.fetchall()
        for r in rows:
            print(r)
    except Exception as e:
        print(f"Ошибка в запросе {i}: {e}")

conn.close()