CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    IF quantity IS NULL OR quantity <= 0 THEN
        RETURN 0;
    END IF;
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER,
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
AS $$
DECLARE
    v_order_id INTEGER;
    v_product_id INTEGER;
    v_price NUMERIC;
BEGIN
    IF p_qty <= 0 THEN
        RAISE NOTICE 'Количество должно быть больше 0';
        RETURN;
    END IF;

    SELECT product_id
    INTO v_product_id
    FROM stock_items
    WHERE stock_item_id = p_stock_item_id;

    IF v_product_id IS NULL THEN
        RAISE NOTICE 'Складская позиция не найдена';
        RETURN;
    END IF;

    SELECT price
    INTO v_price
    FROM products
    WHERE product_id = v_product_id;

    INSERT INTO orders(user_id, order_date)
    VALUES (p_user_id, NOW())
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items(order_id, product_id, quantity, price, stock_item_id)
    VALUES (v_order_id, v_product_id, p_qty, v_price, p_stock_item_id);

    UPDATE stock_items
    SET quantity_available = quantity_available - p_qty
    WHERE stock_item_id = p_stock_item_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_stock_pg(
    p_stock_item_id INTEGER,
    p_delta INTEGER
)
AS $$
DECLARE
    v_current INTEGER;
BEGIN
    SELECT quantity_available
    INTO v_current
    FROM stock_items
    WHERE stock_item_id = p_stock_item_id;

    IF v_current IS NULL THEN
        RAISE NOTICE 'Складская позиция не найдена';
        RETURN;
    END IF;

    IF v_current + p_delta < 0 THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
        RETURN;
    END IF;

    UPDATE stock_items
    SET quantity_available = quantity_available + p_delta
    WHERE stock_item_id = p_stock_item_id;

EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Произошла ошибка: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id      INTEGER,
    p_stock_item_id INTEGER,
    p_qty          INTEGER
)
AS $$
DECLARE
    v_product_id INTEGER;
    v_price      NUMERIC;
    v_order_id   INTEGER;
    v_available  INTEGER;
BEGIN
    SELECT quantity_available, product_id
      INTO v_available, v_product_id
      FROM stock_items
     WHERE stock_item_id = p_stock_item_id;

    IF v_product_id IS NULL THEN
        RAISE NOTICE 'Позиция склада % не найдена', p_stock_item_id;
        RETURN;
    END IF;

    IF v_available < p_qty THEN
        RAISE NOTICE 'Недостаточно товара: есть %, нужно %', v_available, p_qty;
        RETURN;
    END IF;

    SELECT price INTO v_price FROM products WHERE product_id = v_product_id;

    INSERT INTO orders (user_id, order_date)
    VALUES (p_user_id, NOW())
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items (order_id, product_id, stock_item_id, quantity, price)
    VALUES (v_order_id, v_product_id, p_stock_item_id, p_qty, v_price);

    UPDATE stock_items
       SET quantity_available = quantity_available - p_qty
     WHERE stock_item_id = p_stock_item_id;

    RAISE NOTICE 'Заказ % создан', v_order_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE write_off_stock(
    p_stock_item_id INTEGER,
    p_qty          INTEGER
)
AS $$
BEGIN
    UPDATE stock_items
       SET quantity_available = quantity_available - p_qty
     WHERE stock_item_id = p_stock_item_id;

    IF (SELECT quantity_available FROM stock_items WHERE stock_item_id = p_stock_item_id) < 0 THEN
        RAISE EXCEPTION 'Недостаточно товара на складе!';
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Недостаточно товара на складе! Ошибка: %', SQLERRM;
        ROLLBACK;
END;
$$ LANGUAGE plpgsql;