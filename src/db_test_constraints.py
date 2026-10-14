"""
Скрипт проверки работы ограничений целостности.
Пытается нарушить каждое ограничение и проверяет, что база отказывает.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe_store.sqlite')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def try_insert(conn, description, sql, params=()):
    """Пытается выполнить INSERT и сообщает результат."""
    try:
        conn.execute(sql, params)
        conn.commit()
        print(f"  ✗ ОШИБКА: {description} — вставка прошла (ограничение не сработало!)")
        return False
    except sqlite3.IntegrityError as e:
        print(f"  ✓ OK: {description} — база отказала: {e}")
        return True


def try_delete(conn, description, sql, params=()):
    """Пытается выполнить DELETE и сообщает результат."""
    try:
        conn.execute(sql, params)
        conn.commit()
        print(f"  ✗ ОШИБКА: {description} — удаление прошло (ограничение не сработало!)")
        return False
    except sqlite3.IntegrityError as e:
        print(f"  ✓ OK: {description} — база отказала: {e}")
        return True


def test_check_constraints(conn):
    print("\n--- Проверка ограничений CHECK ---")

    try_insert(conn,
        "товар с ценой -100",
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ('Тестовый товар', -100)
    )

    try_insert(conn,
        "товар с пустым наименованием",
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ('', 1000)
    )

    try_insert(conn,
        "товарная позиция с количеством -5",
        "INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (?, ?, ?)",
        (1, 8, -5)
    )

    try_insert(conn,
        "позиция заказа с количеством 0",
        "INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)",
        (1, 1, 0, 100)
    )

    try_insert(conn,
        "пользователь с логином из 2 символов",
        "INSERT INTO users (role_id, login, password_hash) VALUES (?, ?, ?)",
        (3, 'ab', 'hash')
    )

    try_insert(conn,
        "размер 100",
        "INSERT INTO sizes (size_value) VALUES (?)",
        (100,)
    )


def test_foreign_keys(conn):
    print("\n--- Проверка ограничений FOREIGN KEY ---")

    try_insert(conn,
        "пользователь с несуществующей ролью",
        "INSERT INTO users (role_id, login, password_hash) VALUES (?, ?, ?)",
        (999, 'testuser', 'hash')
    )

    try_insert(conn,
        "товарная позиция с несуществующим товаром",
        "INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (?, ?, ?)",
        (999, 1, 10)
    )

    try_delete(conn,
        "удаление роли, на которую ссылаются пользователи",
        "DELETE FROM roles WHERE id = ?",
        (3,)
    )

    try_delete(conn,
        "удаление пользователя, у которого есть заказы",
        "DELETE FROM users WHERE id = ?",
        (3,)
    )

    try_delete(conn,
        "удаление товара, у которого есть позиции",
        "DELETE FROM products WHERE id = ?",
        (1,)
    )


def test_cascade(conn):
    print("\n--- Проверка каскадного удаления ---")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (user_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)",
        (3, '2024-04-01 12:00:00', 'new', 1000)
    )
    temp_order_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)",
        (temp_order_id, 1, 1, 1000)
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (temp_order_id,))
    before = cursor.fetchone()[0]
    print(f"  Позиций до удаления заказа: {before}")

    cursor.execute("DELETE FROM orders WHERE id = ?", (temp_order_id,))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (temp_order_id,))
    after = cursor.fetchone()[0]
    print(f"  Позиций после удаления заказа: {after}")

    if before > 0 and after == 0:
        print("  ✓ OK: каскадное удаление работает")
    else:
        print("  ✗ ОШИБКА: каскадное удаление не работает")


def main():
    print("=" * 60)
    print("ПРОВЕРКА ОГРАНИЧЕНИЙ ЦЕЛОСТНОСТИ")
    print("=" * 60)

    conn = get_connection()

    test_check_constraints(conn)
    test_foreign_keys(conn)
    test_cascade(conn)

    conn.close()

    print("\n" + "=" * 60)
    print("ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == '__main__':
    main()