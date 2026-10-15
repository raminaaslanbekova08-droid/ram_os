"""Экспорт схемы БД в db/schema.sql."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"

conn = sqlite3.connect(DB_PATH)
rows = conn.execute(
    "SELECT sql FROM sqlite_master "
    "WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' "
    "ORDER BY CASE type WHEN 'table' THEN 1 WHEN 'index' THEN 2 ELSE 3 END;"
).fetchall()
conn.close()

with open(SCHEMA_PATH, "w", encoding="utf-8") as f:
    f.write("-- schema.sql — структура БД shoe_store\n\n")
    for (sql,) in rows:
        f.write(sql.strip() + ";\n\n")

print(f"[ok] Схема сохранена в {SCHEMA_PATH}")