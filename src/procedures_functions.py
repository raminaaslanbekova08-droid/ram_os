import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"


def calc_order_total(price, quantity):
    """Функция-калькулятор: цена * количество. Если quantity <= 0, вернуть 0."""
    if price is None or quantity is None:
        return 0
    if quantity <= 0:
        return 0
    return float(price) * int(quantity)


def get_category_count(conn, category_name):
    """Возвращает количество товаров в категории."""
    if category_name is None:
        return 0
    row = conn.execute(
        "SELECT COUNT(*) FROM products WHERE category = ?",
        (category_name,)
    ).fetchone()
    return row[0]


def format_phone(phone):
    """89991234567 -> +7 (999) 123-45-67. Если формат неверный — вернуть исходную строку."""
    if phone is None:
        return phone
    s = str(phone).strip()
    digits = "".join(ch for ch in s if ch.isdigit())

    if len(digits) == 11 and digits[0] in ("7", "8"):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    if len(digits) == 10:
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    return s


def register_functions(conn):
    """Регистрирует Python-функции внутри SQLite."""
    conn.create_function("calculate_total", 2, calc_order_total)
    conn.create_function(
        "count_in_category", 1,
        lambda category: get_category_count(conn, category)
    )
    conn.create_function("format_phone", 1, format_phone)


def table_columns(conn, table):
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]


def insert_row(conn, table, data):
    """Вставляет только те поля, которые реально есть в таблице."""
    cols = [c for c in data if c in table_columns(conn, table)]
    if not cols:
        raise ValueError(f"Нет подходящих колонок для {table}")
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['?'] * len(cols))})"
    cur = conn.execute(sql, tuple(data[c] for c in cols))
    return cur.lastrowid


def create_order(conn, user_id, stock_item_id, qty):
    """
    Эмуляция процедуры create_order:
    1) проверка остатка;
    2) INSERT в orders;
    3) INSERT в order_items;
    4) UPDATE stock_items;
    5) commit/rollback.
    """
    if qty <= 0:
        print("Количество должно быть > 0")
        return False

    try:
        conn.execute("BEGIN IMMEDIATE")

        row = conn.execute(
            "SELECT quantity_available FROM stock_items WHERE stock_item_id = ?",
            (stock_item_id,)
        ).fetchone()

        if row is None:
            conn.rollback()
            print("Позиция склада не найдена")
            return False

        if row[0] < qty:
            conn.rollback()
            print("Недостаточно товара на складе")
            return False

        order_data = {
            "user_id": user_id,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "new",
        }
        order_id = insert_row(conn, "orders", order_data)

        item_data = {
            "order_id": order_id,
            "stock_item_id": stock_item_id,
            "quantity": qty,
        }

        item_cols = table_columns(conn, "order_items")
        if "price" in item_cols or "unit_price" in item_cols:
            price_row = conn.execute("""
                SELECT p.price
                FROM stock_items s
                JOIN products p ON p.product_id = s.product_id
                WHERE s.stock_item_id = ?
            """, (stock_item_id,)).fetchone()
            if price_row:
                if "price" in item_cols:
                    item_data["price"] = price_row[0]
                if "unit_price" in item_cols:
                    item_data["unit_price"] = price_row[0]

        insert_row(conn, "order_items", item_data)

        conn.execute(
            "UPDATE stock_items SET quantity_available = quantity_available - ? "
            "WHERE stock_item_id = ?",
            (qty, stock_item_id)
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка create_order: {e}")
        return False


def update_stock(conn, stock_item_id, delta):
    """
    Эмуляция процедуры update_stock.
    delta может быть отрицательной. Если остаток уходит в минус — rollback.
    """
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT quantity_available FROM stock_items WHERE stock_item_id = ?",
            (stock_item_id,)
        ).fetchone()
        if row is None:
            conn.rollback()
            print("Позиция склада не найдена")
            return False

        new_qty = row[0] + delta
        if new_qty < 0:
            conn.rollback()
            print("Остаток не может быть отрицательным")
            return False

        conn.execute(
            "UPDATE stock_items SET quantity_available = ? WHERE stock_item_id = ?",
            (new_qty, stock_item_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка update_stock: {e}")
        return False


def get_sales_report(conn, date_from=None, date_to=None):
    """Возвращает отчёт по продажам."""
    sql = """
        SELECT
            o.order_id,
            o.order_date,
            u.login,
            SUM(oi.quantity) AS total_qty,
            SUM(oi.quantity * p.price) AS total_amount
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN stock_items s ON s.stock_item_id = oi.stock_item_id
        JOIN products p ON p.product_id = s.product_id
        LEFT JOIN users u ON u.user_id = o.user_id
        WHERE 1 = 1
    """
    params = []
    if date_from:
        sql += " AND o.order_date >= ?"
        params.append(date_from)
    if date_to:
        sql += " AND o.order_date <= ?"
        params.append(date_to)
    sql += " GROUP BY o.order_id, o.order_date, u.login ORDER BY o.order_id"
    return conn.execute(sql, params).fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    register_functions(conn)

    print("calculate_total(1000, 3) =", conn.execute("SELECT calculate_total(1000, 3)").fetchone()[0])
    print("calculate_total(1000, 0) =", conn.execute("SELECT calculate_total(1000, 0)").fetchone()[0])
    print("format_phone('89991234567') =", conn.execute("SELECT format_phone('89991234567')").fetchone()[0])

    print("\nКатегории и количество:")
    for row in conn.execute("""
        SELECT category, count_in_category(category)
        FROM products
        GROUP BY category
        ORDER BY category
    """):
        print(row)

    print("\nОтчёт по продажам:")
    for row in get_sales_report(conn):
        print(row)

    conn.close()