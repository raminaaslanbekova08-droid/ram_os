"""
db_clear.py — удаляет все данные из таблиц, но не трогает структуру.
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"

TABLES = [
    "order_items", "orders", "stock_items",
    "products", "users", "sizes", "roles",
]


def main():
    if not DB_PATH.exists():
        print(f"[!] Нет файла БД: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        for t in TABLES:
            conn.execute(f"DELETE FROM {t};")
        try:
            conn.execute("DELETE FROM sqlite_sequence;")
        except sqlite3.OperationalError:
            pass
        conn.commit()
        print("[ok] Все данные удалены, структура сохранена.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()