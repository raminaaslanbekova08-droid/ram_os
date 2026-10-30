
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    changed_at TEXT NOT NULL DEFAULT (datetime('now'))
);


ALTER TABLE users ADD COLUMN updated_at TEXT;



DROP TRIGGER IF EXISTS trg_products_price_audit;
CREATE TRIGGER trg_products_price_audit
AFTER UPDATE OF price ON products
FOR EACH ROW
WHEN OLD.price <> NEW.price
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value, new_value, changed_at)
    VALUES (
        'products',
        'UPDATE',
        NEW.product_id,
        CAST(OLD.price AS TEXT),
        CAST(NEW.price AS TEXT),
        datetime('now')
    );
END;

DROP TRIGGER IF EXISTS trg_orders_delete_audit;
CREATE TRIGGER trg_orders_delete_audit
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value, new_value, changed_at)
    VALUES (
        'orders',
        'DELETE',
        OLD.order_id,
        NULL,
        NULL,
        datetime('now')
    );
END;

DROP TRIGGER IF EXISTS trg_users_updated_at;
CREATE TRIGGER trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
WHEN NEW.updated_at IS OLD.updated_at -- защита от рекурсии
BEGIN
    UPDATE users
    SET updated_at = datetime('now')
    WHERE user_id = NEW.user_id;
END;


DROP TRIGGER IF EXISTS trg_order_items_stock;
CREATE TRIGGER trg_order_items_stock
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE stock_items
    SET quantity_available = quantity_available - NEW.quantity
    WHERE stock_item_id = NEW.stock_item_id;
END;


DROP TRIGGER IF EXISTS trg_users_no_delete_with_orders;
CREATE TRIGGER trg_users_no_delete_with_orders
BEFORE DELETE ON users
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM orders WHERE user_id = OLD.user_id
)
BEGIN
    SELECT RAISE(ABORT, 'Нельзя удалить пользователя с активными заказами');
END;

DROP TRIGGER IF EXISTS trg_stock_no_negative_insert;
CREATE TRIGGER trg_stock_no_negative_insert
BEFORE INSERT ON stock_items
FOR EACH ROW
WHEN NEW.quantity_available < 0
BEGIN
    SELECT RAISE(ABORT, 'Количество не может быть отрицательным');
END;