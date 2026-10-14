PRAGMA foreign_keys = ON;

CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            stock_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price REAL NOT NULL CHECK (price > 0),
            FOREIGN KEY (order_id) REFERENCES orders(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (stock_item_id) REFERENCES stock_items(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL DEFAULT (datetime('now'))
                CHECK (date(order_date) IS NOT NULL),
            status TEXT NOT NULL DEFAULT 'new'
                CHECK (status IN ('new', 'paid', 'shipped', 'completed', 'cancelled')),
            total_amount REAL DEFAULT 0 CHECK (total_amount >= 0),
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL CHECK (length(name) > 0),
            description TEXT,
            price REAL NOT NULL
                CHECK (price > 0 AND price < 1000000),
            category TEXT,
            manufacturer TEXT,
            image_path TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

CREATE TABLE roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE CHECK (length(name) > 0),
            description TEXT
        );

CREATE TABLE sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size_value REAL NOT NULL UNIQUE
                CHECK (size_value > 20 AND size_value < 50),
            size_system TEXT DEFAULT 'EU'
        );

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE stock_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            quantity_available INTEGER NOT NULL DEFAULT 0
                CHECK (quantity_available >= 0),
            UNIQUE (product_id, size_id),
            FOREIGN KEY (product_id) REFERENCES products(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE,
            FOREIGN KEY (size_id) REFERENCES sizes(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL,
            login TEXT NOT NULL UNIQUE
                CHECK (length(login) >= 3 AND length(login) <= 20),
            password_hash TEXT NOT NULL CHECK (length(password_hash) > 0),
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (role_id) REFERENCES roles(id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

CREATE INDEX idx_order_items_order_id ON order_items(order_id);

CREATE INDEX idx_order_items_stock_item_id ON order_items(stock_item_id);

CREATE INDEX idx_orders_order_date ON orders(order_date);

CREATE INDEX idx_orders_user_id ON orders(user_id);

CREATE INDEX idx_products_category ON products(category);

CREATE INDEX idx_products_manufacturer ON products(manufacturer);

CREATE INDEX idx_products_name ON products(name);

CREATE INDEX idx_stock_items_product_id ON stock_items(product_id);

CREATE INDEX idx_stock_items_size_id ON stock_items(size_id);

CREATE INDEX idx_users_login ON users(login);

CREATE INDEX idx_users_role_id ON users(role_id);
