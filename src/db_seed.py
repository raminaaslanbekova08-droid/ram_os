"""
Скрипт заполнения базы данных тестовыми данными.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe_store.sqlite')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def seed_roles(conn):
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
        [
            ('admin', 'Администратор системы'),
            ('manager', 'Менеджер магазина'),
            ('customer', 'Покупатель'),
        ]
    )
    conn.commit()
    print("Роли добавлены.")


def seed_users(conn):
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT OR IGNORE INTO users
           (role_id, login, password_hash, first_name, last_name, email)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (1, 'admin', 'hash_admin_123', 'Иван', 'Иванов', 'admin@example.com'),
            (2, 'manager1', 'hash_manager_1', 'Пётр', 'Петров', 'manager@example.com'),
            (3, 'user1', 'hash_user_1', 'Анна', 'Сидорова', 'anna@example.com'),
            (3, 'user2', 'hash_user_2', 'Олег', 'Кузнецов', 'oleg@example.com'),
        ]
    )
    conn.commit()
    print("Пользователи добавлены.")


def seed_sizes(conn):
    cursor = conn.cursor()
    sizes = [(36,), (37,), (38,), (39,), (40,), (41,), (42,), (43,), (44,), (45,)]
    cursor.executemany(
        "INSERT OR IGNORE INTO sizes (size_value) VALUES (?)",
        sizes
    )
    conn.commit()
    print("Размеры добавлены.")


def seed_products(conn):
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT OR IGNORE INTO products
           (name, description, price, category, manufacturer, image_path)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            ('Кроссовки Nike Air', 'Спортивные кроссовки', 8999.00, 'кроссовки', 'Nike', 'images/nike_air.jpg'),
            ('Туфли Classic', 'Классические туфли', 5499.00, 'туфли', 'Ecco', 'images/ecco_classic.jpg'),
            ('Ботинки Winter', 'Зимние ботинки', 12999.00, 'ботинки', 'Timberland', 'images/timberland.jpg'),
            ('Сандалии Summer', 'Летние сандалии', 2999.00, 'сандалии', 'Adidas', 'images/adidas_summer.jpg'),
            ('Кеды Urban', 'Городские кеды', 4599.00, 'кеды', 'Converse', 'images/converse.jpg'),
        ]
    )
    conn.commit()
    print("Товары добавлены.")


def seed_stock_items(conn):
    cursor = conn.cursor()
    items = []
    for product_id in range(1, 6):
        for size_id in [3, 4, 5, 6, 7]:
            items.append((product_id, size_id, 10))

    cursor.executemany(
        """INSERT OR IGNORE INTO stock_items
           (product_id, size_id, quantity_available)
           VALUES (?, ?, ?)""",
        items
    )
    conn.commit()
    print("Товарные позиции добавлены.")


def seed_orders(conn):
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT INTO orders (user_id, order_date, status, total_amount)
           VALUES (?, ?, ?, ?)""",
        [
            (3, '2024-01-15 10:30:00', 'completed', 8999.00),
            (3, '2024-02-20 14:15:00', 'paid', 5499.00),
            (4, '2024-03-10 09:00:00', 'new', 12999.00),
        ]
    )
    conn.commit()
    print("Заказы добавлены.")


def seed_order_items(conn):
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT INTO order_items (order_id, stock_item_id, quantity, price)
           VALUES (?, ?, ?, ?)""",
        [
            (1, 1, 1, 8999.00),
            (2, 6, 1, 5499.00),
            (3, 11, 1, 12999.00),
            (3, 12, 1, 12999.00),
        ]
    )
    conn.commit()
    print("Позиции заказов добавлены.")


def seed_all():
    print("=" * 60)
    print("ЗАПОЛНЕНИЕ БАЗЫ ТЕСТОВЫМИ ДАННЫМИ")
    print("=" * 60)

    conn = get_connection()

    seed_roles(conn)
    seed_users(conn)
    seed_sizes(conn)
    seed_products(conn)
    seed_stock_items(conn)
    seed_orders(conn)
    seed_order_items(conn)

    cursor = conn.cursor()
    for table in ['roles', 'users', 'sizes', 'products', 'stock_items', 'orders', 'order_items']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} записей")

    conn.close()
    print("\nБаза данных заполнена.")


if __name__ == '__main__':
    seed_all()