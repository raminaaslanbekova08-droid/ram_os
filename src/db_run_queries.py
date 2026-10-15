"""Выполняет queries/04_check_queries.sql и печатает результаты."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "shoe_store.sqlite"
QUERIES_PATH = BASE_DIR / "queries" / "04_check_queries.sql"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        script = f.read()

    cleaned_lines = []
    for line in script.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines)

    queries = [q.strip() for q in cleaned.split(";") if q.strip()]

    for i, query in enumerate(queries, 1):
        print(f"\n=== Запрос {i} ===")
        print(query)
        print("-" * 40)
        try:
            rows = conn.execute(query).fetchall()
            if not rows:
                print("(пусто)")
            else:
                print(" | ".join(rows[0].keys()))
                for r in rows:
                    print(" | ".join(str(v) for v in r))
        except sqlite3.Error as e:
            print(f"[!] Ошибка: {e}")

    conn.close()


if __name__ == "__main__":
    main()