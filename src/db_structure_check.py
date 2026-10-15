"""
db_structure_check.py — автоматическая проверка структуры БД.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"

EXPECTED_TABLES = [
    "roles", "sizes", "users", "products",
    "stock_items", "orders", "order_items",
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name;"
    ).fetchall()
    return [r["name"] for r in rows]


def get_columns(conn, table):
    return conn.execute(f"PRAGMA table_info({table});").fetchall()


def get_foreign_keys(conn, table):
    return conn.execute(f"PRAGMA foreign_key_list({table});").fetchall()


def get_indexes(conn, table):
    return conn.execute(f"PRAGMA index_list({table});").fetchall()


def check_database() -> bool:
    conn = get_connection()
    ok = True
    try:
        tables = get_tables(conn)
        print(f"Найдено таблиц: {len(tables)} -> {tables}")
        for t in EXPECTED_TABLES:
            if t not in tables:
                print(f"  [!] НЕТ таблицы: {t}")
                ok = False

        print("\n--- Структура таблиц ---")
        for t in EXPECTED_TABLES:
            if t not in tables:
                continue
            cols = get_columns(conn, t)
            fks = get_foreign_keys(conn, t)
            idxs = get_indexes(conn, t)
            print(f"\n[{t}] полей: {len(cols)}")
            for c in cols:
                pk = "PK" if c["pk"] else "  "
                notnull = "NOT NULL" if c["notnull"] else "NULL"
                print(f"   {pk} {c['name']:<20} {c['type']:<8} {notnull}")
            if fks:
                print("   Внешние ключи:")
                for fk in fks:
                    print(f"     {fk['from']} -> {fk['table']}({fk['to']}) "
                          f"ON DELETE {fk['on_delete']}")
            if idxs:
                print("   Индексы:")
                for ix in idxs:
                    print(f"     {ix['name']} unique={ix['unique']}")
        return ok
    finally:
        conn.close()


if __name__ == "__main__":
    if check_database():
        print("\n[OK] Структура корректна.")
    else:
        print("\n[FAIL] Есть проблемы со структурой.")