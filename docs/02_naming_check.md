import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe_store.sqlite')

 Список зарезервированных слов SQL (основные)
RESERVED_WORDS = {
    'select', 'from', 'where', 'order', 'group', 'by', 'having', 'insert', 'update', 
    'delete', 'create', 'drop', 'alter', 'table', 'index', 'view', 'join', 'inner', 
    'left', 'right', 'full', 'on', 'as', 'and', 'or', 'not', 'null', 'is', 'in', 
    'like', 'between', 'exists', 'all', 'any', 'some', 'union', 'except', 'intersect',
    'case', 'when', 'then', 'else', 'end', 'primary', 'key', 'foreign', 'references',
    'check', 'unique', 'default', 'integer', 'text', 'real', 'blob', 'numeric'
}

def get_tables(cursor):
    """Возвращает список всех таблиц в базе данных."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row[0] for row in cursor.fetchall()]

def get_columns(cursor, table_name):
    """Возвращает список всех полей таблицы."""
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [row[1] for row in cursor.fetchall()]

def check_name(name):
    """Проверяет одно имя на соответствие правилам."""
    errors = []
    
     1. Начинается с буквы
    if not name[0].isalpha():
        errors.append("Имя должно начинаться с буквы.")
    
     2. Только строчные латинские буквы, цифры и подчёркивание
    if not re.match(r'^[a-z][a-z0-9_]*$', name):
        errors.append("Имя должно содержать только строчные латинские буквы, цифры и подчёркивание (snake_case).")
    
     3. Не является зарезервированным словом
    if name.lower() in RESERVED_WORDS:
        errors.append(f"Имя '{name}' является зарезервированным словом SQL.")
        
    return errors

def check_database():
    """Проходит по всем таблицам и полям, собирает отчёт."""
    if not os.path.exists(DB_PATH):
        print(f"База данных не найдена по пути: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tables = get_tables(cursor)
    report = []
    has_errors = False

    print("--- Проверка схемы именования ---")
    
    for table in tables:
         Проверка имени таблицы
        table_errors = check_name(table)
        if table_errors:
            has_errors = True
            report.append(f"Таблица '{table}': {', '.join(table_errors)}")
        
         Проверка имён полей
        columns = get_columns(cursor, table)
        for col in columns:
            col_errors = check_name(col)
            if col_errors:
                has_errors = True
                report.append(f"  Поле '{table}.{col}': {', '.join(col_errors)}")
    
    if not has_errors:
        print("Все имена таблиц и полей соответствуют требованиям.")
    else:
        print("Обнаружены ошибки в именовании:")
        for line in report:
            print(line)
            
    conn.close()

if __name__ == "__main__":
    check_database()