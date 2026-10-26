DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS stock_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sizes;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    last_name   TEXT    NOT NULL,
    first_name  TEXT    NOT NULL,
    login       TEXT    NOT NULL UNIQUE,
    password    TEXT    NOT NULL,
    email       TEXT,
    phone       TEXT
);


CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name TEXT    NOT NULL UNIQUE
);


CREATE TABLE manufacturers (
    manufacturer_id   INTEGER PRIMARY KEY,
    manufacturer_name TEXT    NOT NULL UNIQUE
);


CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT    NOT NULL,
    category     TEXT    NOT NULL,
    manufacturer TEXT    NOT NULL,
    price        REAL    NOT NULL,
    description  TEXT
);


CREATE TABLE sizes (
    size_id    INTEGER PRIMARY KEY,
    size_value REAL    NOT NULL UNIQUE
);


CREATE TABLE stock_items (
    stock_item_id INTEGER PRIMARY KEY,
    product_id    INTEGER NOT NULL,
    size_id       INTEGER NOT NULL,
    quantity      INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id)    REFERENCES sizes(size_id),
    UNIQUE (product_id, size_id)
);


CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL,
    order_date TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status     TEXT    NOT NULL DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    size_id       INTEGER,
    quantity      INTEGER NOT NULL,
    price         REAL    NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id)    REFERENCES sizes(size_id)
);