SELECT u.user_id,
       u.last_name,
       u.first_name,
       u.login,
       r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id
ORDER BY u.user_id;


SELECT product_id,
       product_name,
       category,
       manufacturer,
       price,
       image_path
FROM products
ORDER BY product_id;


SELECT size_id, size_value
FROM sizes
ORDER BY size_value;


SELECT o.order_id,
       o.order_date,
       o.status,
       u.last_name || ' ' || u.first_name AS client_name
FROM orders o
JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_date;


SELECT si.stock_item_id,
       p.product_name,
       s.size_value,
       si.quantity
FROM stock_items si
JOIN products p ON si.product_id = p.product_id
JOIN sizes    s ON si.size_id    = s.size_id
ORDER BY p.product_name, s.size_value;


SELECT o.order_id,
       o.order_date,
       u.last_name || ' ' || u.first_name AS client_name,
       SUM(oi.quantity * oi.price) AS total_sum
FROM orders o
JOIN users       u  ON o.user_id       = u.user_id
JOIN order_items oi ON oi.order_id     = o.order_id
GROUP BY o.order_id
ORDER BY o.order_id;
