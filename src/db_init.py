import sqlite3, os, random
from datetime import datetime, timedelta

DB_PATH = "db/shoe_store.sqlite"
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    login TEXT UNIQUE,
    role_id INTEGER REFERENCES roles(role_id),
    updated_at TEXT,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_name TEXT
);

CREATE TABLE IF NOT EXISTS stock_items (
    stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(product_id),
    size_id INTEGER REFERENCES sizes(size_id),
    quantity_available INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    order_date TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id),
    stock_item_id INTEGER REFERENCES stock_items(stock_item_id),
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
""")

for r in ["admin_db", "developer", "reader"]:
    cur.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (r,))

for s in ["39", "40", "41", "42", "43", "44"]:
    cur.execute("INSERT INTO sizes (size_name) VALUES (?)", (s,))

products = [
    ("Кроссовки Nike Air", 8500.0, "Кроссовки"),
    ("Ботинки Timberland", 12000.0, "Ботинки"),
    ("Туфли Classic", 6500.0, "Туфли"),
    ("Сандалии Summer", 3200.0, "Сандалии"),
    ("Кеды Converse", 5400.0, "Кеды"),
]
cur.executemany("INSERT INTO products (product_name, price, category) VALUES (?, ?, ?)", products)

cur.execute("SELECT product_id FROM products")
pid_list = [r[0] for r in cur.fetchall()]
cur.execute("SELECT size_id FROM sizes")
sid_list = [r[0] for r in cur.fetchall()]
for pid in pid_list:
    for sid in sid_list:
        cur.execute("INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (?, ?, ?)",
                    (pid, sid, 10))

cur.execute("SELECT role_id, role_name FROM roles")
roles_map = {name: rid for rid, name in cur.fetchall()}
users = [
    ("Иванов", "Иван", "Иванович", "ivanov", roles_map["reader"]),
    ("Петров", "Пётр", None, "petrov", roles_map["developer"]),
    ("Сидорова", "Анна", "Сергеевна", "sidorova", roles_map["admin_db"]),
    ("Смирнов", "Алексей", None, "smirnov", roles_map["reader"]),
]
cur.executemany(
    "INSERT INTO users (last_name, first_name, middle_name, login, role_id) VALUES (?, ?, ?, ?, ?)",
    users
)

cur.execute("SELECT user_id FROM users")
uids = [r[0] for r in cur.fetchall()]
cur.execute("SELECT product_id, price FROM products")
prods = cur.fetchall()
cur.execute("SELECT stock_item_id, product_id FROM stock_items")
stock_map = {}
for si, pid in cur.fetchall():
    stock_map.setdefault(pid, si)

for i in range(6):
    uid = random.choice(uids)
    dt = (datetime.now() - timedelta(days=random.randint(1, 200))).strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO orders (user_id, order_date) VALUES (?, ?)", (uid, dt))
    oid = cur.lastrowid
    for _ in range(random.randint(1, 3)):
        pid, price = random.choice(prods)
        qty = random.randint(1, 2)
        cur.execute("INSERT INTO order_items (order_id, product_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?, ?)",
                    (oid, pid, stock_map[pid], qty, price))

conn.commit()
conn.close()
print("База инициализирована:", DB_PATH)