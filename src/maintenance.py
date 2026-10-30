import sqlite3
from pathlib import Path
from backup_restore import DB_PATH, backup_safe, check_integrity

def get_db_stats(conn):
    print("\n📊 СБОР СТАТИСТИКИ БАЗЫ ДАННЫХ")
    
    page_size = conn.execute("PRAGMA page_size;").fetchone()[0]
    page_count = conn.execute("PRAGMA page_count;").fetchone()[0]
    total_size = page_size * page_count
    
    print(f"Размер страницы: {page_size} байт")
    print(f"Количество страниц: {page_count}")
    print(f"Общий размер базы (примерный): {total_size} байт ({round(total_size/1024, 2)} КБ)")
    
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';").fetchall()
    print("Список таблиц:")
    for t in tables:
        print(f" - {t[0]}")

def clear_old_logs(conn, days=30):
    print(f"\n🧹 ОЧИСТКА ЛОГОВ СТАРШЕ {days} ДНЕЙ")
    try:
        cursor = conn.execute("""
            DELETE FROM audit_log 
            WHERE changed_at < date('now', '-' || ? || ' days')
        """, (days,))
        conn.commit()
        print(f"Удалено старых записей: {cursor.rowcount}")
    except sqlite3.OperationalError:
        print("Таблица audit_log еще не создана или произошла ошибка.")

if __name__ == "__main__":
    print("🚀 ЗАПУСК СКРИПТА ОБСЛУЖИВАНИЯ БД")
    
    conn = sqlite3.connect(DB_PATH)
    check_integrity(conn)
    conn.close()
    
    print("\n💾 РЕЗЕРВНОЕ КОПИРОВАНИЕ")
    backup_safe()
    
    conn = sqlite3.connect(DB_PATH)
    get_db_stats(conn)
    clear_old_logs(conn, days=30)
    conn.close()
    
    print("\n✅ Обслуживание успешно завершено!")