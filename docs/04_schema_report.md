 Отчёт о структуре базы данных (Схема)

 Порядок создания таблиц
Таблицы создаются строго с учетом зависимостей:
1. `roles` (справочник)
2. `sizes` (справочник)
3. `users` (FK на `roles`)
4. `products` (независимая)
5. `stock_items` (FK на `products`, `sizes`)
6. `orders` (FK на `users`)
7. `order_items` (FK на `orders`, `stock_items`)

 Описание таблиц

 1. roles
*   **Поля:** `role_id` (INTEGER, PK AUTOINCREMENT), `role_name` (TEXT, NOT NULL, UNIQUE).
*   **Первичный ключ:** `role_id`
*   **Внешние ключи:** нет.
*   **Индексы:** нет (UNIQUE создает автоиндекс).

 2. sizes
*   **Поля:** `size_id` (INTEGER, PK AUTOINCREMENT), `size_value` (REAL, NOT NULL, UNIQUE, CHECK > 20 AND < 50).
*   **Первичный ключ:** `size_id`
*   **Внешние ключи:** нет.
*   **Индексы:** нет.

 3. users
*   **Поля:** `user_id` (INTEGER, PK AUTOINCREMENT), `last_name` (TEXT, NOT NULL), `first_name` (TEXT, NOT NULL), `middle_name` (TEXT), `login` (TEXT, NOT NULL, UNIQUE, CHECK length 3-20), `role_id` (INTEGER, NOT NULL).
*   **Первичный ключ:** `user_id`
*   **Внешние ключи:** `role_id` → `roles(role_id)` ON DELETE RESTRICT.
*   **Индексы:** `idx_users_role_id`.

 4. products
*   **Поля:** `product_id` (INTEGER, PK AUTOINCREMENT), `category` (TEXT, NOT NULL), `subcategory` (TEXT), `manufacturer` (TEXT, NOT NULL), `product_name` (TEXT, NOT NULL, CHECK непустое), `image_path` (TEXT), `composition` (TEXT), `description` (TEXT), `price` (REAL, NOT NULL, CHECK > 0 AND < 1000000).
*   **Первичный ключ:** `product_id`
*   **Внешние ключи:** нет.
*   **Индексы:** `idx_products_category`.

 5. stock_items
*   **Поля:** `stock_item_id` (INTEGER, PK AUTOINCREMENT), `product_id` (INTEGER, NOT NULL), `size_id` (INTEGER, NOT NULL), `quantity_available` (INTEGER, NOT NULL, DEFAULT 0, CHECK >= 0).
*   **Первичный ключ:** `stock_item_id`
*   **Внешние ключи:** `product_id` → `products(product_id)` ON DELETE RESTRICT; `size_id` → `sizes(size_id)` ON DELETE RESTRICT.
*   **Индексы:** `idx_stock_items_product_id`, `idx_stock_items_size_id`.

 6. orders
*   **Поля:** `order_id` (INTEGER, PK AUTOINCREMENT), `order_date` (TEXT, NOT NULL), `user_id` (INTEGER, NOT NULL).
*   **Первичный ключ:** `order_id`
*   **Внешние ключи:** `user_id` → `users(user_id)` ON DELETE RESTRICT.
*   **Индексы:** `idx_orders_user_id`, `idx_orders_order_date`.

 7. order_items
*   **Поля:** `order_item_id` (INTEGER, PK AUTOINCREMENT), `order_id` (INTEGER, NOT NULL), `stock_item_id` (INTEGER, NOT NULL), `quantity` (INTEGER, NOT NULL, CHECK > 0), `price` (REAL, NOT NULL, CHECK > 0).
*   **Первичный ключ:** `order_item_id`
*   **Внешние ключи:** `order_id` → `orders(order_id)` ON DELETE CASCADE; `stock_item_id` → `stock_items(stock_item_id)` ON DELETE RESTRICT.
*   **Индексы:** `idx_order_items_order_id`, `idx_order_items_stock_item_id`.