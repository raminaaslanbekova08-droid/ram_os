"""
db_drop.py — полностью удаляет файл базы данных.
Полезно при пересоздании БД с нуля.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[ok] Файл БД удалён: {DB_PATH}")
    else:
        print(f"[skip] Файла нет: {DB_PATH}")


if __name__ == "__main__":
    main()