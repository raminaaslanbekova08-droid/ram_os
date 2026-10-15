"""
Экспорт структуры базы в SQL-файл.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"
OUT_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"


def export_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT sql FROM sqlite_master
        WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'
        ORDER BY
            CASE type
                WHEN 'table' THEN 1
                WHEN 'index' THEN 2
                ELSE 3
            END,
            name
    """)
    statements = [row[0] for row in cur.fetchall()]
    conn.close()

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("-- Схема базы данных shoe_store\n")
        f.write("-- Автоматически сгенерировано\n\n")
        f.write("PRAGMA foreign_keys = ON;\n\n")
        for stmt in statements:
            f.write(stmt.strip() + ";\n\n")

    print(f"Схема экспортирована в {OUT_PATH}")


if __name__ == "__main__":
    export_schema()