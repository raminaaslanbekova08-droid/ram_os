"""
Скрипт проверки соблюдения правил именования объектов БД.
"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
INDEX_PATTERN = re.compile(r"^idx_[a-z][a-z0-9_]*$")


def check_naming() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT name, type FROM sqlite_master
        WHERE name NOT LIKE 'sqlite_%'
          AND type IN ('table', 'index')
        ORDER BY type, name;
    """)
    rows = cur.fetchall()
    conn.close()

    errors = []
    for name, obj_type in rows:
        if obj_type == "table":
            if not SNAKE_CASE.match(name):
                errors.append(f"Таблица '{name}' не соответствует snake_case")
            if not name.endswith("s") and name not in ("audit_log",):
                errors.append(f"Таблица '{name}' не во множественном числе")
        elif obj_type == "index":
            if not INDEX_PATTERN.match(name):
                errors.append(f"Индекс '{name}' не соответствует шаблону idx_<table>_<column>")

    if errors:
        print("Найдены проблемы именования:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Все имена объектов БД корректны.")


if __name__ == "__main__":
    check_naming()