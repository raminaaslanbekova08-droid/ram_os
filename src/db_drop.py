import os
from db_init import DB_PATH


def drop_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Файл базы данных удалён: {DB_PATH}")
    else:
        print(f"Файл базы данных не найден: {DB_PATH}")


if __name__ == "__main__":
    drop_db()