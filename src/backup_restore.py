import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"
BACKUP_DIR = BASE_DIR / "db" / "backups"

def backup_simple():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backup_path = BACKUP_DIR / f"backup_simple_{timestamp}.sqlite"
    
    shutil.copy2(DB_PATH, backup_path)
    print(f"✅ Бэкап (shutil) создан: {backup_path.name}")
    return backup_path

def backup_safe():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backup_path = BACKUP_DIR / f"backup_safe_{timestamp}.sqlite"
    
    source = sqlite3.connect(DB_PATH)
    target = sqlite3.connect(backup_path)
    
    try:
        source.backup(target)
        print(f"✅ Бэкап (safe API) создан: {backup_path.name}")
    finally:
        target.close()
        source.close()
    
    return backup_path

def check_integrity(conn):
    print("🔍 Проверка целостности базы (PRAGMA integrity_check)...")
    result = conn.execute("PRAGMA integrity_check;").fetchone()[0]
    
    if result == "ok":
        print("✅ База данных здорова (статус: ok).")
    else:
        print(f"❌ Найдены ошибки: {result}")
    return result

def restore(backup_path):
    backup_path = Path(backup_path)
    if not backup_path.exists():
        print(f"❌ Файл бэкапа {backup_path} не найден!")
        return
        
    print(f"⚠️ Восстанавливаем БД из {backup_path.name}...")
    shutil.copy2(backup_path, DB_PATH)
    print("✅ База данных успешно восстановлена!")

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    
    check_integrity(conn)
    conn.close()
    
    b1 = backup_simple()
    b2 = backup_safe()