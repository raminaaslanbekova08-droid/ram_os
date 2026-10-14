 Индексы базы данных

| Таблица | Поле | Тип | Обоснование |
| :--- | :--- | :--- | :--- |
| users | role_id | обычный | Ускоряет JOIN с таблицей roles |
| orders | user_id | обычный | Ускоряет JOIN с таблицей users |
| orders | order_date | обычный | Ускоряет сортировку заказов по дате |
| products | category | обычный | Ускоряет фильтрацию по категории |
| products | manufacturer | обычный | Ускоряет фильтрацию по производителю |
| stock_items | product_id | обычный | Ускоряет JOIN с таблицей products |
| stock_items | size_id | обычный | Ускоряет JOIN с таблицей sizes |
| order_items | order_id | обычный | Ускоряет JOIN с таблицей orders |
| order_items | stock_item_id | обычный | Ускоряет JOIN с таблицей stock_items |