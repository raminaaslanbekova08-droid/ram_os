SELECT
    o.order_id,
    o.order_date,
    u.last_name,
    u.first_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_id;


SELECT
    si.stock_item_id,
    p.product_name,
    s.size_value
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes    s ON si.size_id   = s.size_id
ORDER BY si.stock_item_id;


SELECT
    o.order_id,
    o.order_date,
    u.last_name,
    u.first_name,
    p.product_name,
    oi.quantity
FROM orders o
INNER JOIN users       u  ON o.user_id        = u.user_id
INNER JOIN order_items oi ON o.order_id       = oi.order_id
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
ORDER BY o.order_id, p.product_name;


SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
ORDER BY u.user_id, o.order_id;



SELECT COUNT(*) AS total_users
FROM users;


SELECT AVG(price) AS avg_price
FROM products;


SELECT
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products;


SELECT SUM(quantity * price) AS total_revenue
FROM order_items;



SELECT
    category,
    COUNT(*) AS products_count
FROM products
GROUP BY category
ORDER BY products_count DESC;


SELECT
    manufacturer,
    AVG(price) AS avg_price
FROM products
GROUP BY manufacturer
ORDER BY avg_price DESC;


SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    SUM(oi.quantity * oi.price) AS total_amount
FROM users u
INNER JOIN orders      o  ON u.user_id        = o.user_id
INNER JOIN order_items oi ON o.order_id       = oi.order_id
GROUP BY u.user_id, u.last_name, u.first_name
ORDER BY total_amount DESC;


SELECT
    p.product_name,
    SUM(oi.quantity) AS pairs_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
ORDER BY pairs_sold DESC;


SELECT
    s.size_value,
    COUNT(si.stock_item_id) AS stock_items_count
FROM sizes s
INNER JOIN stock_items si ON s.size_id = si.size_id
GROUP BY s.size_value
ORDER BY s.size_value;




SELECT
    category,
    COUNT(*) AS models_count
FROM products
GROUP BY category
HAVING COUNT(*) > 3;


SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    COUNT(o.order_id) AS orders_count
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name
HAVING COUNT(o.order_id) > 2
ORDER BY orders_count DESC;


SELECT
    p.product_name,
    SUM(oi.quantity * oi.price) AS total_sales
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000
ORDER BY total_sales DESC;




SELECT
    s.size_value,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN sizes       s  ON si.size_id       = s.size_id
GROUP BY s.size_value
ORDER BY total_sold DESC
LIMIT 3;


SELECT
    u.user_id,
    u.last_name,
    u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL
ORDER BY u.user_id;


SELECT AVG(order_total) AS avg_order_amount
FROM (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.price) AS order_total
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
) AS order_sums;


SELECT
    p.manufacturer,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.manufacturer
ORDER BY total_revenue DESC
LIMIT 1;