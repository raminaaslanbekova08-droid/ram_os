import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

PERMISSIONS = {
    "admin_db": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader": ["SELECT"]
}

def seed_roles(conn):
    """Добавляет роли в таблицу roles, если их там еще нет."""
    roles_to_add = ["admin_db", "developer", "reader"]
    for role_name in roles_to_add:
        existing = conn.execute(
            "SELECT role_id FROM roles WHERE role_name = ?", (role_name,)
        ).fetchone()
        
        if not existing:
            conn.execute("INSERT INTO roles (role_name) VALUES (?)", (role_name,))
            print(f"Роль '{role_name}' добавлена в базу.")
        else:
            print(f"Роль '{role_name}' уже существует.")
    conn.commit()

def check_permission(conn, user_id, action):
    """
    Принимает ID пользователя и действие (например, 'DELETE').
    Возвращает True, если роль позволяет действие, иначе False.
    """
    action = action.upper()
    
    row = conn.execute("""
        SELECT r.role_name 
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.user_id = ?
    """, (user_id,)).fetchone()

    if not row:
        print(f"Пользователь с ID {user_id} не найден или у него нет роли.")
        return False

    role_name = row[0]
    
    allowed_actions = PERMISSIONS.get(role_name, [])
    
    if action in allowed_actions:
        print(f"Пользователю {user_id} (роль: {role_name}) РАЗРЕШЕНО действие {action}.")
        return True
    else:
        print(f"Пользователю {user_id} (роль: {role_name}) ЗАПРЕЩЕНО действие {action}.")
        return False

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    
    seed_roles(conn)
    
    print("\n--- Тестирование прав ---")
    
    reader = conn.execute("""
        SELECT u.user_id FROM users u 
        JOIN roles r ON u.role_id = r.role_id 
        WHERE r.role_name = 'reader' LIMIT 1
    """).fetchone()
    
    admin = conn.execute("""
        SELECT u.user_id FROM users u 
        JOIN roles r ON u.role_id = r.role_id 
        WHERE r.role_name = 'admin_db' LIMIT 1
    """).fetchone()

    if reader:
        check_permission(conn, reader[0], "DELETE") 
        check_permission(conn, reader[0], "SELECT") 
    else:
        print("В базе нет пользователя с ролью 'reader'.")

    if admin:
        check_permission(conn, admin[0], "DELETE") 
    else:
        print("В базе нет пользователя с ролью 'admin_db'.")

    conn.close()