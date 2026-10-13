import sqlite3
import os


DB_PATH = os.path.join("db", "shoe_store.sqlite")


def get_connection():
    """Возвращает соединение с БД SQLite с включённой проверкой внешних ключей."""
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Создаёт все семь таблиц в правильном порядке."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    -- 1. Справочник ролей
    CREATE TABLE IF NOT EXISTS roles (
        role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT    NOT NULL UNIQUE
    );

    -- 2. Справочник размеров
    CREATE TABLE IF NOT EXISTS sizes (
        size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        size_value REAL    NOT NULL UNIQUE
    );

    -- 3. Товары
    CREATE TABLE IF NOT EXISTS products (
        product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT    NOT NULL,
        category     TEXT    NOT NULL,
        manufacturer TEXT    NOT NULL,
        price        NUMERIC(10, 2) NOT NULL CHECK (price > 0),
        image_path   TEXT
    );

    -- 4. Пользователи
    CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name   TEXT    NOT NULL,
        first_name  TEXT    NOT NULL,
        middle_name TEXT,
        login       TEXT    NOT NULL UNIQUE,
        role_id     INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
    );

    -- 5. Товарные позиции (товар + размер + количество)
    CREATE TABLE IF NOT EXISTS stock_items (
        stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id    INTEGER NOT NULL,
        size_id       INTEGER NOT NULL,
        quantity      INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (size_id)    REFERENCES sizes(size_id)
    );

    -- 6. Заказы
    CREATE TABLE IF NOT EXISTS orders (
        order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        order_date TEXT    NOT NULL DEFAULT (DATE('now')),
        status     TEXT    NOT NULL DEFAULT 'new',
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
    );

    -- 7. Состав заказа
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id      INTEGER NOT NULL,
        stock_item_id INTEGER NOT NULL,
        quantity      INTEGER NOT NULL CHECK (quantity > 0),
        price         NUMERIC(10, 2) NOT NULL CHECK (price > 0),
        FOREIGN KEY (order_id)      REFERENCES orders(order_id)      ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"База данных создана: {DB_PATH}")