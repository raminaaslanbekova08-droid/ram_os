CREATE VIEW v_orders_full AS
SELECT 
    o.order_id,
    o.order_date,
    u.last_name || ' ' || u.first_name AS full_name,
    SUM(oi.price * oi.quantity) AS order_total
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.order_date, u.user_id, u.last_name, u.first_name;

GO

CREATE VIEW v_products_with_stock AS
SELECT 
    p.product_name,
    p.price,
    s.value AS size_value,
    si.quantity AS stock_quantity
FROM products p
JOIN stock_items si ON si.product_id = p.product_id
JOIN sizes s ON s.size_id = si.size_id;

GO

CREATE VIEW v_user_stats AS
SELECT 
    u.last_name || ' ' || u.first_name AS full_name,
    u.login,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.login;

GO



CREATE INDEX idx_products_category 
ON products (category);

GO

CREATE INDEX idx_orders_order_date 
ON orders (order_date);

GO

CREATE INDEX idx_orders_user_id 
ON orders (user_id);

GO

CREATE INDEX idx_stock_items_product_id 
ON stock_items (product_id);

GO

CREATE INDEX idx_stock_items_size_id 
ON stock_items (size_id);

GO

CREATE INDEX idx_products_manufacturer_category 
ON products (manufacturer, category);