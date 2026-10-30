import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

def hash_password(password):
    """Превращает пароль в SHA-256 хэш (длинную строку из 64 символов)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def setup_db(conn):
    cols = [r[1] for r in conn.execute("PRAGMA table_info(users)")]
    if "password_hash" not in cols:
        conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        print("Колонка password_hash добавлена в таблицу users.")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS login_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            status TEXT NOT NULL,
            login_time TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

def log_login_attempt(conn, login, status):
    conn.execute(
        "INSERT INTO login_audit (login, status) VALUES (?, ?)",
        (login, status)
    )
    conn.commit()

def register_user(conn, login, password, role_id=3):
    """Регистрирует пользователя, сохраняя только хэш пароля."""
    pwd_hash = hash_password(password)
    
    try:
        conn.execute(
            "INSERT INTO users (login, password_hash, role_id) VALUES (?, ?, ?)",
            (login, pwd_hash, role_id)
        )
        conn.commit()
        print(f"Пользователь {login} успешно зарегистрирован.")
        return True
    except sqlite3.IntegrityError:
        print(f"Ошибка: Пользователь с логином {login} уже существует.")
        return False

def check_password(conn, login, password):
    """Сравнивает введенный пароль с хэшем в базе и пишет результат в аудит."""
    row = conn.execute(
        "SELECT password_hash FROM users WHERE login = ?", 
        (login,)
    ).fetchone()

    if not row or row[0] is None:
        log_login_attempt(conn, login, "failure")
        return False

    stored_hash = row[0]
    input_hash = hash_password(password)

    if stored_hash == input_hash:
        log_login_attempt(conn, login, "success")
        return True
    else:
        log_login_attempt(conn, login, "failure")
        return False

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    setup_db(conn)

    print("\n--- Тестирование регистрации и входа ---")
    
    register_user(conn, "admin_test", "superpassword123")
    
    print("Вход с правильным паролем:", check_password(conn, "admin_test", "superpassword123"))
    
    print("Вход с неправильным паролем:", check_password(conn, "admin_test", "wrongpassword"))
    
    print("\n--- Данные в таблице login_audit ---")
    for row in conn.execute("SELECT login, status, login_time FROM login_audit"):
        print(row)

    conn.close()