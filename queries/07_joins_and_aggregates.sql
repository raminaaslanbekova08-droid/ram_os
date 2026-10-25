SELECT o.order_id, o.order_date, u.last_name, u.first_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id;

SELECT si.stock_item_id, p.product_name, s.size_value
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes s ON si.size_id = s.size_id;

SELECT o.order_id, u.last_name, u.first_name, p.product_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id;

SELECT u.user_id, u.last_name, u.first_name, o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id;


SELECT COUNT(*) AS total_users FROM users;

SELECT AVG(price) AS avg_price FROM products;

SELECT MIN(price) AS min_price, MAX(price) AS max_price FROM products;

SELECT SUM(quantity * price) AS total_revenue FROM order_items;


SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;

SELECT manufacturer, AVG(price) AS avg_price
FROM products
GROUP BY manufacturer;

SELECT u.user_id, u.last_name, u.first_name,
       SUM(oi.quantity * oi.price) AS total_spent
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.last_name, u.first_name;

SELECT p.product_name, SUM(oi.quantity) AS pairs_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id
GROUP BY p.product_name;

SELECT s.size_value, COUNT(*) AS stock_count
FROM stock_items si
INNER JOIN sizes s ON si.size_id = s.size_id
GROUP BY s.size_value;


SELECT category, COUNT(*) AS model_count
FROM products
GROUP BY category
HAVING COUNT(*) > 3;

SELECT u.user_id, u.last_name, u.first_name,
       COUNT(o.order_id) AS order_count
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name
HAVING COUNT(o.order_id) > 2;

SELECT p.product_name, SUM(oi.quantity * oi.price) AS total_sales
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id
GROUP BY p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000;


SELECT s.size_value, SUM(oi.quantity) AS total_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN sizes s ON si.size_id = s.size_id
GROUP BY s.size_value
ORDER BY total_sold DESC
LIMIT 3;

SELECT u.user_id, u.last_name, u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id

WHERE o.order_id IS NULL;

SELECT AVG(order_total) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.price) AS order_total
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
);

SELECT p.manufacturer, SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id
GROUP BY p.manufacturer
ORDER BY total_revenue DESC
LIMIT 1;