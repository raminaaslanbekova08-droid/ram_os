 Отчёт о структуре БД (день 4)

 Таблицы в порядке создания

| № | Таблица      | Назначение                                   |
|---|--------------|----------------------------------------------|
| 1 | roles        | Роли пользователей                           |
| 2 | sizes        | Размеры обуви                                |
| 3 | users        | Пользователи системы                         |
| 4 | products     | Товары                                       |
| 5 | stock_items  | Складские позиции (товар + размер + кол-во)  |
| 6 | orders       | Заказы                                       |
| 7 | order_items  | Позиции заказов                              |


 Детали по таблицам

 roles
- Поля: role_id (PK AUTOINCREMENT), role_name (TEXT NOT NULL UNIQUE).
- Ограничения: NOT NULL, UNIQUE.
- Индексы: нет.

 sizes
- Поля: size_id (PK AUTOINCREMENT), size_value (REAL NOT NULL UNIQUE).
- Ограничения: NOT NULL, UNIQUE, CHECK (20 < size_value < 50).
- Индексы: нет.

 users
- Поля: user_id (PK), last_name, first_name, middle_name, login, role_id.
- FK: role_id → roles(role_id) ON DELETE RESTRICT.
- Ограничения: NOT NULL, UNIQUE (login), CHECK (login 3–20).
- Индексы: idx_users_role.

 products
- Поля: 9 полей (см. db_init.py).
- Ограничения: NOT NULL, CHECK (product_name не пустое), CHECK (0 < price < 1 000 000).
- Индексы: idx_products_category.

 stock_items
- Поля: stock_item_id (PK), product_id, size_id, quantity_available.
- FK: product_id → products RESTRICT; size_id → sizes RESTRICT.
- Ограничения: NOT NULL, DEFAULT 0, CHECK (qty ≥ 0), UNIQUE (product_id, size_id).
- Индексы: idx_stock_product, idx_stock_size.

 orders
- Поля: order_id (PK), order_date, user_id.
- FK: user_id → users ON DELETE RESTRICT.
- Ограничения: NOT NULL, DEFAULT date('now').
- Индексы: idx_orders_user, idx_orders_date.

 order_items
- Поля: order_item_id (PK), order_id, stock_item_id, quantity, price.
- FK: order_id → orders ON DELETE CASCADE; stock_item_id → stock_items ON DELETE RESTRICT.
- Ограничения: NOT NULL, CHECK (quantity > 0), CHECK (price > 0).
- Индексы: idx_items_order, idx_items_stock.