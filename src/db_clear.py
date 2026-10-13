from db_init import get_connection


def clear_all():
    conn = get_connection()
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = OFF;")

    for table in ("order_items", "orders", "stock_items",
                  "users", "products", "sizes", "roles"):
        c.execute(f"DELETE FROM {table};")
        c.execute("DELETE FROM sqlite_sequence WHERE name = ?;", (table,))

    c.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()
    print("Все таблицы очищены.")


if __name__ == "__main__":
    clear_all()