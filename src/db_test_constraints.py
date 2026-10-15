"""
db_test_constraints.py — практическая проверка ограничений БД.
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


def _expect_error(func, description: str) -> dict:
    try:
        func()
        result, status = "ошибки НЕ было", "НЕ ПРОЙДЕН"
    except sqlite3.Error as e:
        result, status = f"ошибка: {e}", "пройден"
    print(f"[{status}] {description}: {result}")
    return {"description": description, "result": result, "status": status}


def test_unique_login():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO roles(role_name) VALUES ('tmp_role');")
            conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                         "VALUES ('A','B','same_login',1);")
            conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                         "VALUES ('C','D','same_login',1);")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "UNIQUE на login")


def test_not_null_last_name():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                         "VALUES (NULL,'B','log1',1);")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "NOT NULL на last_name")


def test_check_price():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO products(category, manufacturer, product_name, price) "
                         "VALUES ('cat','man','name',-5);")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "CHECK на price")


def test_check_quantity():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO products(category, manufacturer, product_name, price) "
                         "VALUES ('cat','man','name',100);")
            conn.execute("INSERT INTO sizes(size_value) VALUES (40);")
            conn.execute("INSERT INTO stock_items(product_id, size_id, quantity_available) "
                         "VALUES (1,1,-3);")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "CHECK на quantity_available")


def test_foreign_key():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                         "VALUES ('X','Y','fkuser',999);")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "FOREIGN KEY на role_id")


def test_on_delete_restrict():
    def action():
        conn = get_connection()
        try:
            conn.execute("INSERT INTO roles(role_name) VALUES ('r1');")
            conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                         "VALUES ('X','Y','restr1',1);")
            conn.execute("DELETE FROM roles WHERE role_id = 1;")
        finally:
            conn.rollback(); conn.close()
    return _expect_error(action, "ON DELETE RESTRICT (roles → users)")


def test_on_delete_cascade() -> dict:
    conn = get_connection()
    status, result = "НЕ ПРОЙДЕН", ""
    try:
        conn.execute("INSERT INTO roles(role_name) VALUES ('r_casc');")
        conn.execute("INSERT INTO users(last_name, first_name, login, role_id) "
                     "VALUES ('U','U','casc_user',1);")
        conn.execute("INSERT INTO products(category, manufacturer, product_name, price) "
                     "VALUES ('c','m','p',100);")
        conn.execute("INSERT INTO sizes(size_value) VALUES (41);")
        conn.execute("INSERT INTO stock_items(product_id, size_id, quantity_available) "
                     "VALUES (1,1,5);")
        conn.execute("INSERT INTO orders(user_id) VALUES (1);")
        conn.execute("INSERT INTO order_items(order_id, stock_item_id, quantity, price) "
                     "VALUES (1,1,2,100);")

        before = conn.execute("SELECT COUNT(*) FROM order_items WHERE order_id=1;").fetchone()[0]
        conn.execute("DELETE FROM orders WHERE order_id = 1;")
        after = conn.execute("SELECT COUNT(*) FROM order_items WHERE order_id=1;").fetchone()[0]

        if before == 1 and after == 0:
            status, result = "пройден", "каскадное удаление сработало"
        else:
            result = f"before={before}, after={after}"
    except sqlite3.Error as e:
        result = f"ошибка: {e}"
    finally:
        conn.rollback(); conn.close()
    print(f"[{status}] ON DELETE CASCADE: {result}")
    return {"description": "ON DELETE CASCADE", "result": result, "status": status}


def main():
    print("=== Проверка ограничений ===\n")
    results = [
        test_unique_login(),
        test_not_null_last_name(),
        test_check_price(),
        test_check_quantity(),
        test_foreign_key(),
        test_on_delete_restrict(),
        test_on_delete_cascade(),
    ]
    print("\n=== Итоговая таблица ===")
    print(f"{'Ограничение':<40}{'Результат':<30}{'Статус'}")
    for r in results:
        print(f"{r['description']:<40}{r['result']:<30}{r['status']}")


if __name__ == "__main__":
    main()