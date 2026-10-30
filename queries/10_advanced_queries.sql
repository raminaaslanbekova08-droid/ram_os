SELECT
    product_name,
    price,
    calc_discount(price, 20) AS discounted_price
FROM products;


SELECT
    format_full_name(last_name, first_name, middle_name) AS fio
FROM users
WHERE middle_name IS NULL OR TRIM(middle_name) = '';


SELECT
    o.order_id,
    pluralize_items(SUM(oi.quantity)) AS items_text
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id;


SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS client,
    calc_discount(SUM(oi.quantity * p.price), 10) AS total_with_discount
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY u.user_id;


SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS client,
    SUM(oi.quantity * p.price) AS total_spent,
    get_client_tier(SUM(oi.quantity * p.price)) AS tier,
    get_client_loyalty_days(MIN(o.order_date)) AS loyalty_days
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY u.user_id;