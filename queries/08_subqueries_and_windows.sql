
SELECT
    product_name,
    price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;


SELECT full_name
FROM (
    SELECT
        u.last_name || ' ' || u.first_name AS full_name,
        ROW_NUMBER() OVER (ORDER BY SUM(oi.price * oi.quantity) DESC) AS rn
    FROM users u
    JOIN orders o        ON o.user_id = u.user_id
    JOIN order_items oi  ON oi.order_id = o.order_id
    GROUP BY u.user_id, u.last_name, u.first_name
) AS ranked_users
WHERE rn = 1;


SELECT u.last_name
FROM users u
WHERE u.user_id IN (SELECT o.user_id FROM orders o)
ORDER BY u.last_name;


SELECT u.last_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
)
ORDER BY u.last_name;


SELECT p.product_name
FROM products p
WHERE p.product_id NOT IN (
    SELECT DISTINCT oi.product_id FROM order_items oi
)
ORDER BY p.product_name;


SELECT
    u.last_name || ' ' || u.first_name AS full_name,
    SUM(oi.price * oi.quantity)        AS total_sum,
    RANK() OVER (ORDER BY SUM(oi.price * oi.quantity) DESC) AS rank
FROM users u
JOIN orders o       ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY u.user_id, u.last_name, u.first_name
ORDER BY rank;


SELECT
    o.order_id,
    u.last_name || ' ' || u.first_name AS full_name,
    o.order_date,
    ROW_NUMBER() OVER (
        PARTITION BY o.user_id
        ORDER BY o.order_date ASC
    ) AS order_number
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY u.last_name, o.order_date;


SELECT
    p.category,
    p.product_name,
    p.price,
    ROW_NUMBER() OVER (
        PARTITION BY p.category
        ORDER BY p.price DESC
    ) AS rn
FROM products p
ORDER BY p.category, rn;


SELECT category, product_name, price
FROM (
    SELECT
        p.category,
        p.product_name,
        p.price,
        ROW_NUMBER() OVER (
            PARTITION BY p.category
            ORDER BY p.price DESC
        ) AS rn
    FROM products p
) AS ranked_products
WHERE rn = 1
ORDER BY category;


SELECT
    o.order_id,
    o.order_date,
    o.order_total,
    SUM(o.order_total) OVER (
        ORDER BY o.order_date, o.order_id
    ) AS running_total
FROM (
    SELECT
        ord.order_id,
        ord.order_date,
        COALESCE(SUM(oi.price * oi.quantity), 0) AS order_total
    FROM orders ord
    LEFT JOIN order_items oi ON oi.order_id = ord.order_id
    GROUP BY ord.order_id, ord.order_date
) AS o
ORDER BY o.order_date, o.order_id;


SELECT
    ord_hist.full_name,
    ord_hist.curr_date,
    ord_hist.prev_date,
    CAST(julianday(ord_hist.curr_date) - julianday(ord_hist.prev_date) AS INT) AS days_diff
FROM (
    SELECT
        u.last_name || ' ' || u.first_name AS full_name,
        o.order_date AS curr_date,
        LAG(o.order_date) OVER (
            PARTITION BY o.user_id
            ORDER BY o.order_date
        ) AS prev_date
    FROM orders o
    JOIN users u ON u.user_id = o.user_id
) AS ord_hist
ORDER BY ord_hist.full_name, ord_hist.curr_date;