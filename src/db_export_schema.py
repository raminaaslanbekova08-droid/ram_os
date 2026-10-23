import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"

def export_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT sql FROM sqlite_master
        WHERE sql IS NOT NULL
          AND type IN ('table', 'index')
          AND name NOT LIKE 'sqlite_%'
        ORDER BY CASE type WHEN 'table' THEN 0 ELSE 1 END, name;
    """)
    
    statements = [row[0] for row in cur.fetchall()]
    conn.close()

    with open(SCHEMA_PATH, "w", encoding="utf-8") as f:
        f.write("PRAGMA foreign_keys = ON;\n\n")
        for stmt in statements:
            f.write(stmt.strip() + ";\n\n")

    print(f"Схема БД успешно экспортирована в {SCHEMA_PATH}")

if __name__ == "__main__":
    export_schema()