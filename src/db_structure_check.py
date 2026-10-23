import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

EXPECTED_TABLES = [
    "roles", "sizes", "users", "products", "stock_items", "orders", "order_items"
]

def get_connection():
    return sqlite3.connect(DB_PATH)

def check_structure():
    conn = get_connection()
    cur = conn.cursor()
    
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    actual_tables = [row[0] for row in cur.fetchall()]
    
    print("--- ПРОВЕРКА ТАБЛИЦ ---")
    for table in EXPECTED_TABLES:
        if table in actual_tables:
            print(f"[OK] Таблица {table} существует.")
            
            cur.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cur.fetchall()]
            print(f"     Поля: {', '.join(columns)}")
            
            cur.execute(f"PRAGMA foreign_key_list({table});")
            fks = cur.fetchall()
            if fks:
                for fk in fks:
                    print(f"     Внешний ключ: {fk[3]} -> {fk[2]}({fk[4]})")
        
            cur.execute(f"PRAGMA index_list({table});")
            idxs = [row[1] for row in cur.fetchall() if not row[1].startswith('sqlite_autoindex')]
            if idxs:
                print(f"     Индексы: {', '.join(idxs)}")
        else:
            print(f"[ОШИБКА] Таблица {table} НЕ НАЙДЕНА!")
            
    conn.close()

if __name__ == "__main__":
    check_structure()