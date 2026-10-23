SELECT * FROM roles;

SELECT u.user_id, u.last_name, u.first_name, u.middle_name, u.login, r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id
ORDER BY u.user_id;

SELECT * FROM products ORDER BY product_id;

SELECT * FROM sizes ORDER BY size_value;

SELECT o.order_id, o.order_date, u.last_name, u.first_name, u.middle_name
FROM orders o
JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_id;

SELECT si.stock_item_id, p.product_name, s.size_value, si.quantity_available
FROM stock_items si
JOIN products p ON si.product_id = p.product_id
JOIN sizes s ON si.size_id = s.size_id
ORDER BY si.stock_item_id;