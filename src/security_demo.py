import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"

def vulnerable_login(conn, login):
    """
    Уязвимость: использование f-строки. 
    Если передать login = "' OR '1'='1", SQL-запрос станет:
    SELECT * FROM users WHERE login = '' OR '1'='1'
    Условие '1'='1' всегда истинно, поэтому вернутся ВСЕ пользователи.
    """
    cursor = conn.cursor()
    query = f"SELECT user_id, login FROM users WHERE login = '{login}'"
    print(f"Выполняется запрос: {query}")
    cursor.execute(query)
    return cursor.fetchall()

def secure_login(conn, login):
    """
    Защита: параметризованный запрос.
    База данных воспринимает символы ? как строгое значение (строку), 
    а не как часть SQL-кода.
    """
    cursor = conn.cursor()
    query = "SELECT user_id, login FROM users WHERE login = ?"
    print(f"Выполняется запрос: {query} с параметром: '{login}'")
    cursor.execute(query, (login,))
    return cursor.fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)

    print("=== 1. Обычный логин (ivanov) ===")
    try:
        print(vulnerable_login(conn, "ivanov"))
    except Exception as e:
        print("Ошибка:", e)

    print("\n=== 2. Атака через уязвимую функцию ===")
    malicious_input = "' OR '1'='1"
    try:
        print(vulnerable_login(conn, malicious_input))
    except Exception as e:
        print("Ошибка:", e)

    print("\n=== 3. Атака через безопасную функцию ===")
    try:
        print(secure_login(conn, malicious_input))
    except Exception as e:
        print("Ошибка:", e)

    conn.close()