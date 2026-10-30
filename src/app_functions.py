import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("db/shoe_store.sqlite")




def _cols(conn, table):
    return [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]


def _first_col(cols, *names):
    for name in names:
        if name in cols:
            return name
    return None


def ensure_schema(conn):
    """Добавляет stock_item_id в order_items, если его нет.
    Это нужно, чтобы cancel_order мог вернуть товар на склад."""
    cols = _cols(conn, "order_items")
    if cols and "stock_item_id" not in cols:
        conn.execute("ALTER TABLE order_items ADD COLUMN stock_item_id INTEGER")
        conn.commit()




def calc_discount(price, discount_percent):
    try:
        if price is None or discount_percent is None:
            return 0.0
        price = float(price)
        discount_percent = float(discount_percent)
    except (TypeError, ValueError):
        return 0.0

    if discount_percent < 0:
        discount_percent = 0
    if discount_percent > 100:
        discount_percent = 100

    return round(price - (price * discount_percent / 100), 2)


def pluralize_items(count):
    try:
        count = int(count)
    except (TypeError, ValueError):
        return "0 товаров"

    if count < 0:
        return "0 товаров"

    n = abs(count)

    if n % 100 in (11, 12, 13, 14):
        return f"{count} товаров"
    if n % 10 == 1:
        return f"{count} товар"
    if n % 10 in (2, 3, 4):
        return f"{count} товара"
    return f"{count} товаров"


def format_full_name(last, first, middle=None):
    if last is None or first is None:
        return "Аноним"

    last = str(last).strip()
    first = str(first).strip()
    middle = "" if middle is None else str(middle).strip()

    if not last or not first:
        return "Аноним"

    last = last.title()
    first_initial = first[0].upper() + "."

    if middle:
        middle_initial = middle[0].upper() + "."
        return f"{last} {first_initial}{middle_initial}"

    return f"{last} {first_initial}"


def get_client_tier(total_spent):
    try:
        if total_spent is None:
            return "Без статуса"
        total_spent = float(total_spent)
    except (TypeError, ValueError):
        return "Без статуса"

    if total_spent < 0:
        return "Без статуса"
    if total_spent < 5000:
        return "Новичок"
    if total_spent < 20000:
        return "Бронза"
    if total_spent < 50000:
        return "Серебро"
    if total_spent < 100000:
        return "Золото"
    return "Платина"


def get_client_loyalty_days(first_order_date_str):
    if not first_order_date_str:
        return 0
    try:
        date_str = str(first_order_date_str).split(" ")[0]
        first_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (datetime.now().date() - first_date).days
    except (ValueError, TypeError):
        return 0




def place_order(conn, user_id, product_id, size_id, quantity):
    try:
        ensure_schema(conn)
        qty = int(quantity)
        if qty <= 0:
            return False

        cur = conn.cursor()

        
        ucols = _cols(conn, "users")
        uid_col = _first_col(ucols, "user_id", "id")
        if not uid_col:
            return False
        user = cur.execute(
            f"SELECT 1 FROM users WHERE {uid_col} = ?", (user_id,)
        ).fetchone()
        if not user:
            return False

        
        scols = _cols(conn, "stock_items")
        sid_col = _first_col(scols, "stock_item_id", "id")
        sprod_col = _first_col(scols, "product_id")
        ssize_col = _first_col(scols, "size_id")
        sqty_col = _first_col(scols, "quantity_available", "quantity")

        if not all([sid_col, sprod_col, ssize_col, sqty_col]):
            return False

        stock_row = cur.execute(
            f"SELECT {sid_col}, {sqty_col} FROM stock_items "
            f"WHERE {sprod_col} = ? AND {ssize_col} = ?",
            (product_id, size_id),
        ).fetchone()

        if not stock_row:
            return False

        stock_item_id, available = stock_row
        if available is None or int(available) < qty:
            print("Недостаточно товара на складе")
            return False

        
        pcols = _cols(conn, "products")
        pid_col = _first_col(pcols, "product_id", "id")
        price_col = _first_col(pcols, "price", "product_price")
        if not pid_col or not price_col:
            return False

        product_row = cur.execute(
            f"SELECT {price_col} FROM products WHERE {pid_col} = ?",
            (product_id,),
        ).fetchone()
        if not product_row:
            return False
        price = product_row[0]

        
        ocols = _cols(conn, "orders")
        oid_col = _first_col(ocols, "order_id", "id")
        ouser_col = _first_col(ocols, "user_id")
        odate_col = _first_col(ocols, "order_date", "created_at", "date")

        if not all([oid_col, ouser_col, odate_col]):
            return False

        cur.execute(
            f"INSERT INTO orders ({ouser_col}, {odate_col}) VALUES (?, ?)",
            (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        order_id = cur.lastrowid

        
        icols = _cols(conn, "order_items")
        iorder_col = _first_col(icols, "order_id")
        iprod_col = _first_col(icols, "product_id")
        iqty_col = _first_col(icols, "quantity")
        iprice_col = _first_col(icols, "price", "unit_price")
        istock_col = _first_col(icols, "stock_item_id")
        isize_col = _first_col(icols, "size_id")

        if not all([iorder_col, iprod_col, iqty_col, iprice_col]):
            raise RuntimeError("В order_items нет нужных колонок")

        insert_cols = [iorder_col, iprod_col, iqty_col, iprice_col]
        insert_vals = [order_id, product_id, qty, price]

        if istock_col:
            insert_cols.append(istock_col)
            insert_vals.append(stock_item_id)
        if isize_col:
            insert_cols.append(isize_col)
            insert_vals.append(size_id)

        placeholders = ",".join(["?"] * len(insert_cols))
        cur.execute(
            f"INSERT INTO order_items ({','.join(insert_cols)}) "
            f"VALUES ({placeholders})",
            insert_vals,
        )

        
        cur.execute(
            f"UPDATE stock_items SET {sqty_col} = {sqty_col} - ? "
            f"WHERE {sid_col} = ?",
            (qty, stock_item_id),
        )

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"place_order error: {e}")
        return False


def cancel_order(conn, order_id):
    try:
        ensure_schema(conn)
        cur = conn.cursor()

        ocols = _cols(conn, "orders")
        oid_col = _first_col(ocols, "order_id", "id")
        if not oid_col:
            return False

        order = cur.execute(
            f"SELECT 1 FROM orders WHERE {oid_col} = ?", (order_id,)
        ).fetchone()
        if not order:
            return False

        icols = _cols(conn, "order_items")
        iorder_col = _first_col(icols, "order_id")
        iprod_col = _first_col(icols, "product_id")
        iqty_col = _first_col(icols, "quantity")
        istock_col = _first_col(icols, "stock_item_id")
        isize_col = _first_col(icols, "size_id")

        scols = _cols(conn, "stock_items")
        sid_col = _first_col(scols, "stock_item_id", "id")
        sprod_col = _first_col(scols, "product_id")
        ssize_col = _first_col(scols, "size_id")
        sqty_col = _first_col(scols, "quantity_available", "quantity")

        if not all([iorder_col, iprod_col, iqty_col, sid_col, sprod_col, sqty_col]):
            return False

        rows = cur.execute(
            f"SELECT {','.join(icols)} FROM order_items WHERE {iorder_col} = ?",
            (order_id,),
        ).fetchall()

        for row in rows:
            data = dict(zip(icols, row))
            qty = int(data.get(iqty_col, 0) or 0)

            if istock_col and data.get(istock_col):
                cur.execute(
                    f"UPDATE stock_items SET {sqty_col} = {sqty_col} + ? "
                    f"WHERE {sid_col} = ?",
                    (qty, data[istock_col]),
                )
            elif isize_col and data.get(isize_col) is not None and ssize_col:
                cur.execute(
                    f"UPDATE stock_items SET {sqty_col} = {sqty_col} + ? "
                    f"WHERE {sprod_col} = ? AND {ssize_col} = ?",
                    (qty, data[iprod_col], data[isize_col]),
                )
            else:
                cur.execute(
                    f"UPDATE stock_items SET {sqty_col} = {sqty_col} + ? "
                    f"WHERE {sid_col} = ("
                    f"  SELECT {sid_col} FROM stock_items "
                    f"  WHERE {sprod_col} = ? LIMIT 1"
                    f")",
                    (qty, data[iprod_col]),
                )

        cur.execute(
            f"DELETE FROM order_items WHERE {iorder_col} = ?", (order_id,)
        )
        cur.execute(f"DELETE FROM orders WHERE {oid_col} = ?", (order_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"cancel_order error: {e}")
        return False



def register_all_functions(conn):
    ensure_schema(conn)
    conn.create_function("calc_discount", 2, calc_discount)
    conn.create_function("pluralize_items", 1, pluralize_items)
    conn.create_function("format_full_name", 3, format_full_name)
    conn.create_function("get_client_tier", 1, get_client_tier)
    conn.create_function("get_client_loyalty_days", 1, get_client_loyalty_days)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    register_all_functions(conn)
    print("Функции зарегистрированы. Пример:")
    print(conn.execute("SELECT calc_discount(1000, 20)").fetchone())
    conn.close()