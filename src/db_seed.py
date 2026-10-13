import sqlite3
from db_init import get_connection, init_db, DB_PATH
import os


def seed():
    if not os.path.exists(DB_PATH):
        init_db()

    conn = get_connection()
    c = conn.cursor()

    c.executemany(
        "INSERT OR IGNORE INTO roles (role_name) VALUES (?)",
        [("admin",), ("manager",), ("user",)]
    )

    c.executemany(
        """
        INSERT OR IGNORE INTO users (last_name, first_name, middle_name, login, role_id)
        VALUES (?, ?, ?, ?, (SELECT role_id FROM roles WHERE role_name = ?))
        """,
        [
            ("Админов", "Админ", None, "admin", "admin"),
            ("Менеджеров", "Менеджер", None, "manager", "manager"),
            ("Пользователев", "Пользователь", None, "user", "user"),
        ]
    )

    c.executemany(
        """
        INSERT OR IGNORE INTO products (product_name, category, manufacturer, price, image_path)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            ("Кроссовки Nike Air", "спорт", "Nike", 7990.00, "images/nike_air.jpg"),
            ("Туфли Clarks", "классика", "Clarks", 12990.00, "images/clarks.jpg"),
            ("Ботинки Timberland", "повседневная", "Timberland", 15990.00, "images/timberland.jpg"),
            ("Сандалии Adidas", "лето", "Adidas", 3990.00, "images/adidas_sandals.jpg"),
            ("Кеды Converse", "спорт", "Converse", 5490.00, "images/converse.jpg"),
        ]
    )

    c.executemany(
        "INSERT OR IGNORE INTO sizes (size_value) VALUES (?)",
        [(36,), (37,), (38,), (39,), (40,)]
    )

    c.executemany(
        """
        INSERT OR IGNORE INTO stock_items (product_id, size_id, quantity)
        VALUES (
            (SELECT product_id FROM products WHERE product_name = ?),
            (SELECT size_id    FROM sizes    WHERE size_value = ?),
            ?
        )
        """,
        [
            ("Кроссовки Nike Air", 39, 10),
            ("Кроссовки Nike Air", 40, 5),
            ("Туфли Clarks", 38, 7),
            ("Туфли Clarks", 39, 3),
            ("Ботинки Timberland", 40, 2),
            ("Сандалии Adidas", 36, 15),
            ("Сандалии Adidas", 37, 8),
            ("Кеды Converse", 38, 12),
            ("Кеды Converse", 39, 6),
            ("Кеды Converse", 40, 4),
        ]
    )

    c.executemany(
        """
        INSERT OR IGNORE INTO orders (user_id, order_date, status)
        VALUES (
            (SELECT user_id FROM users WHERE login = ?),
            ?, ?
        )
        """,
        [
            ("admin", "2024-01-15", "completed"),
            ("manager", "2024-02-20", "processing"),
            ("user", "2024-03-05", "new"),
        ]
    )

    c.executemany(
        """
        INSERT OR IGNORE INTO order_items (order_id, stock_item_id, quantity, price)
        VALUES (
            (SELECT order_id FROM orders WHERE order_date = ?),
            (SELECT stock_item_id FROM stock_items
                WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                  AND size_id    = (SELECT size_id    FROM sizes    WHERE size_value = ?)),
            ?,
            (SELECT price FROM products WHERE product_name = ?)
        )
        """,
        [
            ("2024-01-15", "Кроссовки Nike Air", 39, 1, "Кроссовки Nike Air"),
            ("2024-01-15", "Кеды Converse", 38, 2, "Кеды Converse"),
            ("2024-02-20", "Туфли Clarks", 38, 1, "Туфли Clarks"),
            ("2024-02-20", "Сандалии Adidas", 36, 1, "Сандалии Adidas"),
            ("2024-03-05", "Ботинки Timberland", 40, 1, "Ботинки Timberland"),
            ("2024-03-05", "Кеды Converse", 40, 1, "Кеды Converse"),
        ]
    )

    conn.commit()

    # --- Итоговый отчёт ---
    print("Тестовые данные вставлены. Количество записей:")
    for table in ("roles", "users", "products", "sizes",
                  "stock_items", "orders", "order_items"):
        cnt = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:15s} -> {cnt}")

    conn.close()


if __name__ == "__main__":
    seed()