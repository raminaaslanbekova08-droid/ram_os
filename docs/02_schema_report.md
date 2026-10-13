 Отчёт о структуре БД

Создано 7 таблиц:
1. `roles` — справочник ролей.
2. `sizes` — справочник размеров.
3. `products` — товары.
4. `users` — пользователи.
5. `stock_items` — товарные позиции (товар + размер + количество).
6. `orders` — заказы.
7. `order_items` — состав заказов.

 Ключи и ограничения
- Первичные ключи: `*_id INTEGER PRIMARY KEY AUTOINCREMENT` во всех таблицах.
- Внешние ключи:
  - `users.role_id → roles.role_id` (ON DELETE RESTRICT)
  - `stock_items.product_id → products.product_id`
 
 