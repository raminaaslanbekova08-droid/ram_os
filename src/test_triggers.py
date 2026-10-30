import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"
SQL_TRIGGERS_PATH = BASE_DIR / "db" / "triggers.sql"


def init_triggers(conn):
    """Выполняет SQL-скрипт с триггерами, если он есть."""
    if SQL_TRIGGERS_PATH.exists():
        with open(SQL_TRIGGERS_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
        try:
            conn.executescript(sql_script)
            print("✅ Триггеры из db/triggers.sql успешно применены.\n")
        except sqlite3.OperationalError as e:
            # Игнорируем ошибку ALTER TABLE, если колонка updated_at уже существует
            if "duplicate column name" in str(e).lower():
                print("ℹ️ Колонка updated_at уже существует. Триггеры применены.\n")
            else:
                print(f"⚠️ Ошибка при применении триггеров: {e}\n")


def table_columns(conn, table):
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]


def insert_row(conn, table, data):
    """Безопасная вставка (только для существующих колонок)."""
    cols = [c for c in data if c in table_columns(conn, table)]
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['?'] * len(cols))})"
    return conn.execute(sql, tuple(data[c] for c in cols)).lastrowid


def test_stock_deduction(conn):
    """Тест 1: Списание остатков при добавлении в order_items."""
    print("--- Тест 1: Списание остатков ---")
    
    user = conn.execute("SELECT user_id FROM users LIMIT 1").fetchone()
    stock = conn.execute("""
        SELECT stock_item_id, quantity_available
        FROM stock_items
        WHERE quantity_available >= 2
        LIMIT 1
    """).fetchone()

    if not user or not stock:
        print("❌ Нет подходящих данных (нужен пользователь и товар на складе >= 2).")
        return

    user_id = user[0]
    stock_item_id, before_qty = stock

    try:
        conn.execute("BEGIN IMMEDIATE")

        order_id = insert_row(conn, "orders", {
            "user_id": user_id,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "new",
        })

        insert_row(conn, "order_items", {
            "order_id": order_id,
            "stock_item_id": stock_item_id,
            "quantity": 2,
        })

        after_qty = conn.execute(
            "SELECT quantity_available FROM stock_items WHERE stock_item_id = ?",
            (stock_item_id,)
        ).fetchone()[0]

        print(f"Остаток до заказа:  {before_qty}")
        print(f"Остаток после:      {after_qty}")
        
        if after_qty == before_qty - 2:
            print("✅ Триггер списания остатков СРАБОТАЛ корректно.\n")
        else:
            print("❌ ОШИБКА: Триггер не списал остатки!\n")
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка при тестировании списания: {e}\n")


def test_delete_protection(conn):
    """Тест 2: Защита от удаления пользователя с заказами."""
    print("--- Тест 2: Защита от удаления ---")

    user_with_order = conn.execute("""
        SELECT u.user_id
        FROM users u
        JOIN orders o ON o.user_id = u.user_id
        LIMIT 1
    """).fetchone()

    if not user_with_order:
        print("❌ Нет пользователя с заказами для проверки защиты.")
        return

    uid = user_with_order[0]

    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (uid,))
        conn.commit()
        print("❌ ОШИБКА: Пользователь удалён! Триггер защиты НЕ сработал.\n")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"✅ Триггер защиты СРАБОТАЛ. Поймана ошибка: {e}\n")
    except Exception as e:
        conn.rollback()
        print(f"⚠️ Неожиданная ошибка: {e}\n")


def show_audit_log(conn):
    """Выводит первые 5 строк из audit_log."""
    print("--- Первые 5 строк audit_log ---")
    try:
        rows = conn.execute("""
            SELECT log_id, table_name, operation, record_id, old_value, new_value, changed_at
            FROM audit_log
            ORDER BY log_id DESC
            LIMIT 5
        """).fetchall()
        
        if not rows:
            print("Таблица audit_log пуста.")
        else:
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Не удалось прочитать audit_log: {e}")
    print()


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    
    init_triggers(conn)

    # Запускаем тесты
    test_stock_deduction(conn)
    test_delete_protection(conn)
    show_audit_log(conn)

    conn.close()


if __name__ == "__main__":
    main()