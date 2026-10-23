import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def seed_data():
    conn = get_connection()
    cur = conn.cursor()

    
    cur.executemany("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", 
                    [("администратор",), ("менеджер",), ("клиент",)])
    
    
    cur.executemany("INSERT OR IGNORE INTO sizes (size_value) VALUES (?)", 
                    [(36.0,), (37.5,), (38.0,), (39.0,), (40.0,)])
    

    cur.executemany("""
        INSERT OR IGNORE INTO users (last_name, first_name, middle_name, login, role_id) 
        VALUES (?, ?, ?, ?, ?)
    """, [
        ("Иванов", "Иван", "Иванович", "admin", 1),
        ("Петров", "Петр", None, "manager", 2),
        ("Сидоров", "Сидор", "Сидорович", "client1", 3)
    ])
    

    cur.executemany("""
        INSERT INTO products (category, manufacturer, product_name, price) 
        VALUES (?, ?, ?, ?)
    """, [
        ("Кроссовки", "Nike", "Air Max", 10000.0),
        ("Туфли", "Ecco", "Soft", 12000.0),
        ("Ботинки", "Timberland", "Winter", 15000.0)
    ])
    
    
    cur.executemany("""
        INSERT INTO stock_items (product_id, size_id, quantity_available) 
        VALUES (?, ?, ?)
    """, [
        (1, 1, 10), (1, 2, 5), (2, 3, 7), (3, 4, 3)
    ])
    
    
    cur.executemany("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", 
                    [("2024-01-10", 1), ("2024-02-15", 2)])
    
    
    cur.executemany("""
        INSERT INTO order_items (order_id, stock_item_id, quantity, price) 
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 1, 10000.0), (1, 2, 2, 10000.0), (2, 3, 1, 12000.0)
    ])

    conn.commit()
    conn.close()
    print("База данных успешно заполнена тестовыми данными.")

if __name__ == "__main__":
    seed_data()