
 Шаг 5. Создать `docs/02_query_results.md`

Предварительно откройте `queries/02_check_queries.sql` в SQLite Viewer и выполните каждый запрос. Пример отчёта:

 Результаты простых запросов

 1. Список всех пользователей с ролями
**SQL:** `SELECT u.user_id, u.last_name, u.first_name, u.login, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id;`
**Результат:** 3 строки — admin/admin, manager/manager, user/user.

 2. Список всех товаров
**SQL:** `SELECT product_id, product_name, category, manufacturer, price FROM products;`
**Результат:** 5 строк — Кроссовки RunFast, Ботинки WinterPro, Туфли Classic, Сандалии Summer, Кеды Street.

 3. Список всех размеров
**SQL:** `SELECT size_id, size_value FROM sizes;`
**Результат:** 5 строк — 36, 37, 38, 39, 40.

 4. Список всех заказов с ФИО клиентов
**SQL:**
```sql
SELECT o.order_id, o.order_date, o.status,
       u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client_fio
FROM orders o
JOIN users u ON o.user_id = u.user_id;