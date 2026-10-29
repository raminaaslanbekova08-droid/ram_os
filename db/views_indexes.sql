
DROP VIEW IF EXISTS v_orders_full;
DROP VIEW IF EXISTS v_products_with_stock;
DROP VIEW IF EXISTS v_user_stats;
DROP VIEW IF EXISTS v_simple;

DROP INDEX IF EXISTS idx_products_category;
DROP INDEX IF EXISTS idx_orders_order_date;
DROP INDEX IF EXISTS idx_orders_user_id;
DROP INDEX IF EXISTS idx_stock_items_product_id;
DROP INDEX IF EXISTS idx_stock_items_size_id;
DROP INDEX IF EXISTS idx_products_manufacturer_category;


CREATE VIEW v_orders_full AS
SELECT
    o.order_id,
    o.order_date,
    COALESCE(u.last_name, '') || ' ' || COALESCE(u.first_name, '') AS client_full_name,
    SUM(oi.quantity * oi.price) AS total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, u.last_name, u.first_name;


CREATE VIEW v_products_with_stock AS
SELECT
    p.model_name,
    p.price,
    s.value       AS size_value,
    si.quantity   AS available_quantity
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN sizes s        ON si.size_id   = s.size_id;


CREATE VIEW v_user_stats AS
SELECT
    COALESCE(u.last_name, '') || ' ' || COALESCE(u.first_name, '') AS client_full_name,
    u.login,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.login;


SELECT * FROM v_orders_full          LIMIT 3;
SELECT * FROM v_products_with_stock  LIMIT 3;
SELECT * FROM v_user_stats           LIMIT 3;


EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';

EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';

EXPLAIN QUERY PLAN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.user_id;



CREATE INDEX idx_products_category
    ON products(category);

CREATE INDEX idx_orders_order_date
    ON orders(order_date);

CREATE INDEX idx_orders_user_id
    ON orders(user_id);


CREATE INDEX idx_stock_items_product_id
    ON stock_items(product_id);


CREATE INDEX idx_stock_items_size_id
    ON stock_items(size_id);

CREATE INDEX idx_products_manufacturer_category
    ON products(manufacturer, category);


SELECT name, tbl_name, sql
FROM sqlite_master
WHERE type = 'index'
  AND name LIKE 'idx_%'
ORDER BY tbl_name, name;


EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';


EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';

EXPLAIN QUERY PLAN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.user_id;


CREATE VIEW v_simple AS
SELECT product_id, price
FROM products;


UPDATE v_simple
SET price = 100
WHERE product_id = 1;

