 Анализ VIEW, INDEX и EXPLAIN QUERY PLAN

 1. Какие представления созданы

В файле `db/views_indexes.sql` созданы три представления:

1. `v_orders_full` — полная информация о заказах:
   - номер заказа;
   - дата заказа;
   - ФИО клиента;
   - итоговая сумма заказа.

2. `v_products_with_stock` — товары с остатками:
   - название модели;
   - цена;
   - размер;
   - доступное количество на складе.

3. `v_user_stats` — статистика по клиентам:
   - ФИО;
   - логин;
   - количество заказов.

Представления нужны, чтобы не писать каждый раз длинные запросы с `JOIN` и `GROUP BY`. Они также скрывают сложную логику и позволяют обращаться к результату как к обычной таблице.

 2. Какие индексы созданы и почему

| Индекс | Таблица | Поля | Зачем создан |
|---|---|---|---|
| `idx_products_category` | `products` | `category` | Ускорение поиска товаров по категории |
| `idx_orders_order_date` | `orders` | `order_date` | Ускорение поиска и сортировки по дате заказа |
| `idx_orders_user_id` | `orders` | `user_id` | Ускорение `JOIN` orders ↔ users |
| `idx_stock_items_product_id` | `stock_items` | `product_id` | Ускорение `JOIN` stock_items ↔ products |
| `idx_stock_items_size_id` | `stock_items` | `size_id` | Ускорение `JOIN` stock_items ↔ sizes |
| `idx_products_category_manufacturer` | `products` | `category, manufacturer` | Составной индекс для поиска по категории и производителю |

В SQLite внешние ключи не индексируются автоматически, поэтому индексы на поля `user_id`, `product_id`, `size_id` созданы вручную.

 3. EXPLAIN QUERY PLAN до создания индексов

 3.1. Поиск товаров по категории

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';
```

Пример результата до индекса:

```text
QUERY PLAN
`--SCAN products
```

`SCAN products` означает полный перебор таблицы `products`. Индекс не используется.

 3.2. Поиск товаров по производителю

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';
```

Пример результата:

```text
QUERY PLAN
`--SCAN products
```

База снова перебирает всю таблицу, потому что отдельного индекса по `manufacturer` нет.

 3.3. JOIN orders и users

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.user_id;
```

Пример результата до индекса на `orders.user_id`:

```text
QUERY PLAN
`--SCAN orders AS o
`--SEARCH users AS u USING INTEGER PRIMARY KEY (rowid=?)
```

Таблица `orders` сканируется полностью, потому что поле `user_id` ещё не проиндексировано.

 4. EXPLAIN QUERY PLAN после создания индексов

 4.1. Поиск товаров по категории

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';
```

Пример результата после создания `idx_products_category`:

```text
QUERY PLAN
`--SEARCH products USING INDEX idx_products_category (category=?)
```

`SEARCH ... USING INDEX` означает, что SQLite использует индекс `idx_products_category`. Полный перебор таблицы больше не выполняется.

 4.2. Поиск товаров по производителю

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';
```

Пример результата:

```text
QUERY PLAN
`--SCAN products
```

Индекс `idx_products_category_manufacturer` создан на пару `(category, manufacturer)`. В условии `WHERE manufacturer = 'Nike'` не указана категория, поэтому составной индекс не может быть эффективно использован: `manufacturer` не является первым столбцом индекса. SQLite снова выполняет `SCAN products`.

Вывод: если нужен быстрый поиск только по `manufacturer`, нужно создать отдельный индекс:

```sql
CREATE INDEX idx_products_manufacturer
ON products(manufacturer);
```

В данной работе этого не требуется, поэтому результат `SCAN` для `manufacturer` ожидаем.

 4.3. JOIN orders и users

Запрос:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.user_id;
```

Пример результата после создания `idx_orders_user_id`:

```text
QUERY PLAN
`--SEARCH orders AS o USING INDEX idx_orders_user_id (user_id=?)
`--SEARCH users AS u USING INTEGER PRIMARY KEY (rowid=?)
```

Теперь для соединения таблиц используется индекс `idx_orders_user_id`. Это ускоряет `JOIN`.

 5. Проверка обновляемости представлений

Было создано простое представление:

```sql
CREATE VIEW v_simple AS
SELECT product_id, price
FROM products;
```

Затем выполнена попытка обновления:

```sql
UPDATE v_simple
SET price = 100
WHERE product_id = 1;
```

Результат в SQLite:

```text
Error: cannot modify v_simple because it is a view
```

Также была выполнена попытка обновить сложное представление:

```sql
UPDATE v_orders_full
SET total_amount = 0
WHERE order_id = 1;
```

Результат:

```text
Error: cannot modify v_orders_full because it is a view
```

Вывод: в SQLite обычные представления (`VIEW`) предназначены только для чтения. Они не хранят данные физически и не обновляются напрямую. Для обновления представлений в SQLite нужно было бы создавать специальные триггеры `INSTEAD OF`, но в рамках данной работы это не требуется.

 6. Общий вывод

Индексы ускоряют операции поиска, соединения таблиц и сортировки:

- `WHERE` по индексированному полю: вместо `SCAN TABLE` появляется `SEARCH TABLE ... USING INDEX`;
- `JOIN` по внешнему ключу: индекс на поле связи ускоряет соединение;
- `ORDER BY` по индексированному полю может выполняться быстрее.

Но индексы не используются автоматически в любом запросе. Например:

- если условие `WHERE` не совпадает с первым столбцом составного индекса, индекс может быть проигнорирован;
- при слишком маленькой таблице SQLite может выбрать полный перебор, считая его дешевле;
- если в запросе участвует большая часть строк таблицы, полный скан может быть быстрее индекса.

Также индексы занимают место на диске и немного замедляют `INSERT`, `UPDATE`, `DELETE`, потому что при изменении данных нужно обновлять и индекс. Поэтому индексировать абсолютно все поля не нужно.

 7. Проверка представлений

Проверочные запросы:

```sql
SELECT * FROM v_orders_full LIMIT 3;
SELECT * FROM v_products_with_stock LIMIT 3;
SELECT * FROM v_user_stats LIMIT 3;
```

Данные выводятся корректно, представления работают как виртуальные таблицы.