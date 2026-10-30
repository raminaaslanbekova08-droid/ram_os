CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN COALESCE(price, 0) * GREATEST(quantity, 0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER,
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INTEGER;
    v_available INTEGER;
BEGIN
    IF p_qty <= 0 THEN
        RAISE NOTICE 'Количество должно быть больше нуля';
        RETURN;
    END IF;

    SELECT quantity_available
      INTO v_available
      FROM stock_items
     WHERE stock_item_id = p_stock_item_id
       FOR UPDATE;

    IF v_available IS NULL THEN
        RAISE NOTICE 'Товар не найден';
        RETURN;
    END IF;

    IF v_available < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
        RETURN;
    END IF;

    INSERT INTO orders(user_id, created_at)
    VALUES(p_user_id, NOW())
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items(order_id, stock_item_id, quantity)
    VALUES(v_order_id, p_stock_item_id, p_qty);

    UPDATE stock_items
       SET quantity_available = quantity_available - p_qty
     WHERE stock_item_id = p_stock_item_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Ошибка create_order_pg: %', SQLERRM;
END;
$$;

CREATE OR REPLACE PROCEDURE write_off_stock_pg(
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_available INTEGER;
BEGIN
    SELECT quantity_available
      INTO v_available
      FROM stock_items
     WHERE stock_item_id = p_stock_item_id
       FOR UPDATE;

    IF v_available IS NULL THEN
        RAISE NOTICE 'Товар не найден';
        RETURN;
    END IF;

    IF v_available < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
        RETURN;
    END IF;

    UPDATE stock_items
       SET quantity_available = quantity_available - p_qty
     WHERE stock_item_id = p_stock_item_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Произошла ошибка: %', SQLERRM;
END;
$$;