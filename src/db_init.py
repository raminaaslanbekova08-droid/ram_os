"""
Финальный DDL-скрипт для создания структуры базы данных shoe_store.
Содержит все таблицы, ограничения, индексы.
Исполняется с нуля: запустил — получил работающую базу.
"""

import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_PATH = os.path.join(DB_DIR, 'shoe-store.sqlite')

os.makedirs(DB_DIR, exist_ok=True)


def get_connection():
    """Создаёт соединение с базой данных и включает внешние ключи."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def drop_all_tables(conn):
    """Удаляет все таблицы, если они существуют (для пересоздания)."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")
    tables = [
        'order_items', 'orders', 'stock_items', 'products',
        'sizes', 'users', 'roles'
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def create_tables(conn):
    """Создаёт все таблицы с ограничениями."""
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE CHECK (length(name) > 0),
            description TEXT
        )
    """)


    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL,
            login TEXT NOT NULL UNIQUE
                CHECK (length(login) >= 3 AND length(login) <= 20),
            password_hash TEXT NOT NULL CHECK (length(password_hash) > 0),
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (role_id) REFERENCES roles(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)


    cursor.execute("""
        CREATE TABLE sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size_value REAL NOT NULL UNIQUE
                CHECK (size_value > 20 AND size_value < 50),
            size_system TEXT DEFAULT 'EU'
        )
    """)

    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL CHECK (length(name) > 0),
            description TEXT,
            price REAL NOT NULL
                CHECK (price > 0 AND price < 1000000),
            category TEXT,
            manufacturer TEXT,
            image_path TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)


    cursor.execute("""
        CREATE TABLE stock_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            quantity_available INTEGER NOT NULL DEFAULT 0
                CHECK (quantity_available >= 0),
            UNIQUE (product_id, size_id),
            FOREIGN KEY (product_id) REFERENCES products(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE,
            FOREIGN KEY (size_id) REFERENCES sizes(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL DEFAULT (datetime('now'))
                CHECK (date(order_date) IS NOT NULL),
            status TEXT NOT NULL DEFAULT 'new'
                CHECK (status IN ('new', 'paid', 'shipped', 'completed', 'cancelled')),
            total_amount REAL DEFAULT 0 CHECK (total_amount >= 0),
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)


    cursor.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            stock_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price REAL NOT NULL CHECK (price > 0),
            FOREIGN KEY (order_id) REFERENCES orders(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (stock_item_id) REFERENCES stock_items(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)

    conn.commit()
    print("Все таблицы созданы.")


def create_indexes(conn):
    """Создаёт индексы для внешних ключей и полей поиска/сортировки."""
    cursor = conn.cursor()

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_product_id ON stock_items(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_size_id ON stock_items(size_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_stock_item_id ON order_items(stock_item_id)")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_manufacturer ON products(manufacturer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_login ON users(login)")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)")

    conn.commit()
    print("Все индексы созданы.")


def verify_structure(conn):
    """Проверяет, что структура создана корректно."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\nСоздано таблиц: {len(tables)}")
    for t in tables:
        print(f"  - {t}")

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'index' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    indexes = [row[0] for row in cursor.fetchall()]
    print(f"\nСоздано индексов: {len(indexes)}")
    for i in indexes:
        print(f"  - {i}")


def init_database():
    """Главная функция: пересоздаёт базу с нуля."""
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ shoe_store")
    print("=" * 60)

    conn = get_connection()
    drop_all_tables(conn)
    create_tables(conn)
    create_indexes(conn)
    verify_structure(conn)
    conn.close()

    print("\nБаза данных успешно создана:")
    print(f"  {DB_PATH}")


if __name__ == '__main__':
    init_database()