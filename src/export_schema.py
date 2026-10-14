import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe-store.sqlite')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    SELECT sql FROM sqlite_master
    WHERE sql IS NOT NULL
    ORDER BY
        CASE type
            WHEN 'table' THEN 1
            WHEN 'index' THEN 2
            WHEN 'trigger' THEN 3
            WHEN 'view' THEN 4
        END,
        name
""")

lines = []
for (sql,) in cur.fetchall():
    lines.append(sql + ";")
    lines.append("")

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write("PRAGMA foreign_keys = ON;\n\n")
    f.write("\n".join(lines))

conn.close()
print(f"Схема экспортирована в {os.path.abspath(OUT_PATH)}")