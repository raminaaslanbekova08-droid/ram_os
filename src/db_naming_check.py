"""
Скрипт автоматической проверки схемы именования базы данных SQLite.
Проверяет имена таблиц и полей на соответствие требованиям демоэкзамена.
"""

import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe_store.sqlite')

RESERVED_WORDS = {
    'select', 'from', 'where', 'insert', 'update', 'delete', 'create',
    'drop', 'alter', 'table', 'index', 'view', 'trigger', 'order',
    'group', 'by', 'having', 'join', 'inner', 'outer', 'left', 'right',
    'on', 'as', 'and', 'or', 'not', 'null', 'is', 'in', 'like', 'between',
    'exists', 'all', 'any', 'some', 'union', 'intersect', 'except',
    'distinct', 'case', 'when', 'then', 'else', 'end', 'primary', 'key',
    'foreign', 'references', 'check', 'default', 'unique', 'constraint',
    'column', 'database', 'values', 'into', 'set', 'limit', 'offset'
}


def get_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect(DB_PATH)


def get_tables(conn):
    """Возвращает список всех таблиц в базе данных."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return [row[0] for row in cursor.fetchall()]


def get_columns(conn, table_name):
    """Возвращает список полей таблицы через PRAGMA table_info."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def check_name(name):
    """
    Проверяет одно имя на соответствие правилам.
    Возвращает список ошибок (пустой список = всё хорошо).
    """
    errors = []

    if not name[0].isalpha():
        errors.append("имя должно начинаться с буквы")

    if not re.match(r'^[a-z][a-z0-9_]*$', name):
        errors.append("имя должно содержать только строчные латинские буквы, цифры и _")

    if name.lower() in RESERVED_WORDS:
        errors.append(f"имя '{name}' является зарезервированным словом SQL")

    if '__' in name:
        errors.append("имя содержит двойное подчёркивание")
    if name.endswith('_'):
        errors.append("имя не должно заканчиваться на _")

    return errors


def check_database():
    """Проходит по всем таблицам и полям, собирает отчёт."""
    if not os.path.exists(DB_PATH):
        print(f"ОШИБКА: База данных не найдена по пути {DB_PATH}")
        print("Сначала создайте базу, запустив src/db_init.py")
        return

    conn = get_connection()
    tables = get_tables(conn)

    if not tables:
        print("В базе данных нет таблиц.")
        conn.close()
        return

    total_errors = 0

    print("=" * 70)
    print("ПРОВЕРКА СХЕМЫ ИМЕНОВАНИЯ БАЗЫ ДАННЫХ")
    print("=" * 70)
    print()

    for table in tables:
        table_errors = check_name(table)
        if table_errors:
            print(f"[ТАБЛИЦА] {table}")
            for err in table_errors:
                print(f"    ✗ {err}")
            total_errors += len(table_errors)
        else:
            print(f"[ТАБЛИЦА] {table} — OK")

        columns = get_columns(conn, table)
        for col in columns:
            col_errors = check_name(col)
            if col_errors:
                print(f"    [ПОЛЕ] {col}")
                for err in col_errors:
                    print(f"        ✗ {err}")
                total_errors += len(col_errors)
            else:
                print(f"    [ПОЛЕ] {col} — OK")
        print()

    conn.close()

    print("=" * 70)
    if total_errors == 0:
        print("РЕЗУЛЬТАТ: Все имена соответствуют требованиям. Ошибок нет.")
    else:
        print(f"РЕЗУЛЬТАТ: Найдено ошибок: {total_errors}")
    print("=" * 70)


if __name__ == '__main__':
    check_database()