import sqlite3
import os

DB_PATH = "db/shoe_store.sqlite"


def run_test(name, query, params=(), expect_error=True):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute(query, params)
        conn.commit()
        if expect_error:
            print(f"[FAIL] {name}: ошибка не возникла")
            return "не пройден", "ошибка не возникла"
        else:
            print(f"[OK]   {name}: выполнено без ошибки")
            return "пройден", "выполнено"
    except sqlite3.Error as e:
        if expect_error:
            print(f"[OK]   {name}: получена ошибка — {e}")
            return "пройден", f"ошибка: {e}"
        else:
            print(f"[FAIL] {name}: неожиданная ошибка — {e}")
            return "не пройден", f"ошибка: {e}"
    finally:
        conn.close()


def prepare_data():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("INSERT OR IGNORE INTO roles (role_id, role_name) VALUES (1, 'admin')")
    conn.execute("INSERT OR IGNORE INTO roles (role_id, role_name) VALUES (2, 'manager')")
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, last_name, first_name, login, role_id) "
        "VALUES (1, 'Ivanov', 'Ivan', 'admin', 1)"
    )
    conn.execute("INSERT OR IGNORE INTO sizes (size_id, size_value) VALUES (1, 42)")
    conn.execute(
        "INSERT OR IGNORE INTO products (product_id, product_name, category, manufacturer, price) "
        "VALUES (1, 'Boot', 'cat', 'man', 5000)"
    )
    conn.execute(
        "INSERT OR IGNORE INTO stock_items (stock_item_id, product_id, size_id, quantity) "
        "VALUES (1, 1, 1, 10)"
    )
    conn.commit()
    conn.close()


def main():
    os.makedirs("docs", exist_ok=True)
    prepare_data()

    results = []

    results.append((
        "UNIQUE на login",
        *run_test(
            "UNIQUE на login",
            "INSERT INTO users (last_name, first_name, login, role_id) VALUES (?, ?, ?, ?)",
            ("Petrov", "Petr", "admin", 1),
        )
    ))

    results.append((
        "NOT NULL на last_name",
        *run_test(
            "NOT NULL на last_name",
            "INSERT INTO users (first_name, login, role_id) VALUES (?, ?, ?)",
            ("Petr", "petr", 1),
        )
    ))

    results.append((
        "CHECK на price",
        *run_test(
            "CHECK на price",
            "INSERT INTO products (product_name, category, manufacturer, price) VALUES (?, ?, ?, ?)",
            ("Test", "cat", "man", -100),
        )
    ))

    results.append((
        "CHECK на quantity",
        *run_test(
            "CHECK на quantity",
            "INSERT INTO stock_items (product_id, size_id, quantity) VALUES (?, ?, ?)",
            (1, 1, -5),
        )
    ))

    results.append((
        "FOREIGN KEY на role_id",
        *run_test(
            "FOREIGN KEY на role_id",
            "INSERT INTO users (last_name, first_name, login, role_id) VALUES (?, ?, ?, ?)",
            ("Sidorov", "Sidr", "sidor", 999),
        )
    ))

    results.append((
        "ON DELETE RESTRICT",
        *run_test(
            "ON DELETE RESTRICT",
            "DELETE FROM roles WHERE role_id = ?",
            (1,),
        )
    ))

    # ON DELETE CASCADE
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("INSERT OR IGNORE INTO orders (order_id, user_id, order_date) VALUES (1, 1, '2024-01-01')")
    conn.execute(
        "INSERT OR IGNORE INTO order_items (order_item_id, order_id, stock_item_id, quantity, price) "
        "VALUES (1, 1, 1, 2, 5000)"
    )
    conn.commit()
    conn.execute("DELETE FROM orders WHERE order_id = 1")
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM order_items WHERE order_id = 1").fetchone()[0]
    conn.close()
    if count == 0:
        print("[OK]   ON DELETE CASCADE: позиции удалены каскадно")
        results.append(("ON DELETE CASCADE", "пройден", "каскадное удаление"))
    else:
        print(f"[FAIL] ON DELETE CASCADE: осталось {count} позиций")
        results.append(("ON DELETE CASCADE", "не пройден", f"осталось {count}"))

    with open("docs/02_constraints_test.md", "w", encoding="utf-8") as f:
        f.write("# Результаты проверки ограничений\n\n")
        f.write("| Ограничение | Ожидаемый результат | Фактический результат | Статус |\n")
        f.write("|-------------|---------------------|-----------------------|--------|\n")
        expected = {
            "UNIQUE на login": "ошибка",
            "NOT NULL на last_name": "ошибка",
            "CHECK на price": "ошибка",
            "CHECK на quantity": "ошибка",
            "FOREIGN KEY на role_id": "ошибка",
            "ON DELETE RESTRICT": "ошибка",
            "ON DELETE CASCADE": "каскадное удаление",
        }
        for name, status, fact in results:
            f.write(f"| {name} | {expected[name]} | {fact} | {status} |\n")

    print("\n Отчёт сохранён: docs/02_constraints_test.md")


if __name__ == "__main__":
    main()