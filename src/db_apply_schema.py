"""
db_apply_schema.py — создаёт новую БД и применяет db/schema.sql.
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"


def main():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Нет файла схемы: {SCHEMA_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        script = f.read()

    conn.executescript(script)
    conn.commit()
    conn.close()

    print(f"[ok] Новая БД создана: {DB_PATH}")
    print(f"[ok] Схема применена из: {SCHEMA_PATH}")


if __name__ == "__main__":
    main()