import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def run_test(test_name, query, params=()):
    conn = get_connection()
    try:
        conn.execute(query, params)
        conn.commit()
        print(f"[ПРОВАЛ] {test_name}: запрос прошел, а должен был упасть с ошибкой!")
    except sqlite3.Error as e:
        print(f"[УСПЕХ] {test_name}: база корректно заблокировала запрос. Ошибка: {e}")
    finally:
        conn.rollback()
        conn.close()

def main():
    print("--- ТЕСТИРОВАНИЕ ОГРАНИЧЕНИЙ ---")
    
    
    run_test("UNIQUE на login", 
             "INSERT INTO users (last_name, first_name, login, role_id) VALUES ('Тест', 'Тест', 'admin', 1)")
    

    run_test("NOT NULL на last_name", 
             "INSERT INTO users (last_name, first_name, login, role_id) VALUES (NULL, 'Тест', 'test1', 1)")
    
    
    run_test("CHECK на price (отрицательная)", 
             "INSERT INTO products (category, manufacturer, product_name, price) VALUES ('Тест', 'Тест', 'Тест', -100)")
    

    run_test("CHECK на quantity (отрицательное)", 
             "INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (1, 1, -5)")

    
    run_test("FOREIGN KEY на role_id (несуществующая роль)", 
             "INSERT INTO users (last_name, first_name, login, role_id) VALUES ('Тест', 'Тест', 'test2', 999)")
    

    run_test("ON DELETE RESTRICT (удаление роли с юзерами)", 
             "DELETE FROM roles WHERE role_id = 1")
             

    conn = get_connection()
    try:

        cur = conn.cursor()
        cur.execute("INSERT INTO orders (order_date, user_id) VALUES ('2024-03-01', 3)")
        order_id = cur.lastrowid
        cur.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, 1, 1, 100)", (order_id,))
        conn.commit()
        

        cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        conn.commit()
        

        cur.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (order_id,))
        if cur.fetchone()[0] == 0:
            print("[УСПЕХ] ON DELETE CASCADE: позиции удалились вместе с заказом.")
        else:
            print("[ПРОВАЛ] ON DELETE CASCADE: позиции остались.")
    except sqlite3.Error as e:
        print(f"[ОШИБКА] ON DELETE CASCADE: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()