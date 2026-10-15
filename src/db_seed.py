"""
db_seed.py — заполнение БД тестовыми данными.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed_roles(conn):
    conn.executemany("INSERT INTO roles(role_name) VALUES (?);",
                     [("администратор",), ("менеджер",), ("авторизованный пользователь",)])


def seed_users(conn):
    conn.executemany(
        "INSERT INTO users(last_name, first_name, middle_name, login, role_id) "
        "VALUES (?, ?, ?, ?, ?);",
        [
            ("Иванов", "Иван", "Иванович", "admin", 1),
            ("Петров", "Пётр", None, "manager1", 2),
            ("Сидоров", "Семён", "Сергеевич", "user1", 3),
        ],
    )


def seed_sizes(conn):
    conn.executemany("INSERT INTO sizes(size_value) VALUES (?);",
                     [(36,), (37,), (38,), (39,), (40,)])


def seed_products(conn):
    conn.executemany(
        "INSERT INTO products(category, subcategory, manufacturer, product_name, "
        "image_path, composition, description, price) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        [
            ("Кроссовки", "Беговые", "Nike", "Air Zoom Pegasus", None,
             "текстиль, резина", "Лёгкие беговые кроссовки", 8990.0),
            ("Кроссовки", "Повседневные", "Adidas", "Superstar", None,
             "кожа, резина", "Классические кроссовки", 7490.0),
            ("Туфли", "Классические", "Ecco", "Helsinki", None,
             "натуральная кожа", "Строгие туфли", 12990.0),
            ("Ботинки", "Зимние", "Timberland", "6-Inch Premium", None,
             "нубук", "Тёплые ботинки", 15990.0),
            ("Сандалии", "Летние", "Birkenstock", "Arizona", None,
             "кожа", "Удобные сандалии", 5990.0),
        ],
    )


def seed_stock_items(conn):
    conn.executemany(
        "INSERT INTO stock_items(product_id, size_id, quantity_available) "
        "VALUES (?, ?, ?);",
        [
            (1,1,10), (1,2,8), (1,3,5),
            (2,2,12), (2,3,7),
            (3,3,4), (3,4,6),
            (4,4,3), (4,5,2),
            (5,5,15),
        ],
    )


def seed_orders(conn):
    conn.executemany("INSERT INTO orders(order_date, user_id) VALUES (?, ?);",
                     [("2025-01-10", 1), ("2025-01-11", 2), ("2025-01-12", 3)])


def seed_order_items(conn):
    conn.executemany(
        "INSERT INTO order_items(order_id, stock_item_id, quantity, price) "
        "VALUES (?, ?, ?, ?);",
        [
            (1,1,1,8990.0),
            (1,4,2,7490.0),
            (2,6,1,12990.0),
            (2,9,1,15990.0),
            (3,10,2,5990.0),
            (3,2,1,8990.0),
        ],
    )


def main():
    conn = get_connection()
    try:
        for t in ["order_items", "orders", "stock_items",
                  "products", "users", "sizes", "roles"]:
            conn.execute(f"DELETE FROM {t};")
        try:
            conn.execute("DELETE FROM sqlite_sequence;")
        except sqlite3.OperationalError:
            pass

        seed_roles(conn)
        seed_users(conn)
        seed_sizes(conn)
        seed_products(conn)
        seed_stock_items(conn)
        seed_orders(conn)
        seed_order_items(conn)
        conn.commit()
        print("[ok] Тестовые данные добавлены.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()