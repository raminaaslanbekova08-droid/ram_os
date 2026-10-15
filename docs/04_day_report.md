 Отчёт за день 4

 Что сделано
- Создан файл БД `db/shoe_store.sqlite`.
- DDL-скрипт реализован в `src/db_init.py`.
- 7 таблиц: roles, sizes, users, products, stock_items, orders, order_items.
- Заданы PK (AUTOINCREMENT), FK (RESTRICT и CASCADE),
  ограничения NOT NULL / UNIQUE / CHECK / DEFAULT.
- Включён `PRAGMA foreign_keys = ON`.
- Созданы 8 индексов.
- Структура проверена через `src/db_structure_check.py` — [OK].
- Ограничения проверены через `src/db_test_constraints.py` — все 7 пройдены.
- Схема экспортирована в `db/schema.sql` через `src/db_generate_schema.py`.
- БД восстановлена с нуля из `db/schema.sql` через `src/db_apply_schema.py`.
- Заполнены тестовые данные (`src/db_seed.py`).
- Выполнены проверочные запросы (`queries/04_check_queries.sql`).

 Принятые решения
1. Порядок таблиц: roles → sizes → users → products → stock_items → orders → order_items.
2. `orders.user_id → RESTRICT` — нельзя удалить пользователя с заказами.
3. `order_items.order_id → CASCADE` — позиции удаляются с заказом.
4. Размер обуви REAL — бывает 36.5.
5. Дата заказа TEXT (ISO 8601) — удобно сортируется.
6. Индексы: на все FK, orders.order_date, products.category.