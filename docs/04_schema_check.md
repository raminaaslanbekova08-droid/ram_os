 Результаты проверки структуры базы данных

Проверка выполнена с помощью скрипта `src/db_structure_check.py`, который анализирует системные таблицы SQLite (`sqlite_master`) и использует команды `PRAGMA`.

 Общие результаты
*   Всего таблиц создано: 7 из 7 ожидаемых.
*   Все таблицы, поля, ключи и индексы соответствуют проекту.

 Детальная проверка по таблицам

| Таблица | Кол-во полей | Первичный ключ | Внешние ключи (FK) | Индексы | Ограничения |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **roles** | 2 | `role_id` | нет | нет | NOT NULL, UNIQUE |
| **sizes** | 2 | `size_id` | нет | нет | NOT NULL, UNIQUE, CHECK |
| **users** | 6 | `user_id` | `role_id` → roles | `idx_users_role_id` | NOT NULL, UNIQUE, CHECK, FK |
| **products** | 9 | `product_id` | нет | `idx_products_category` | NOT NULL, CHECK |
| **stock_items** | 4 | `stock_item_id` | `product_id` → products, `size_id` → sizes | `idx_stock_items_product_id`, `idx_stock_items_size_id` | NOT NULL, DEFAULT, CHECK, FK |
| **orders** | 3 | `order_id` | `user_id` → users | `idx_orders_user_id`, `idx_orders_order_date` | NOT NULL, FK |
| **order_items** | 5 | `order_item_id` | `order_id` → orders, `stock_item_id` → stock_items | `idx_order_items_order_id`, `idx_order_items_stock_item_id` | NOT NULL, CHECK, FK |

**Статус:** Структура базы данных полностью корректна и соответствует DDL-скрипту.