 Проверка схемы именования

Правила: имя начинается с буквы; только латиница, цифры и `_`;
нижний регистр; не зарезервированное слово SQL; таблица — во множественном
числе; поле — в единственном; идентификатор — с суффиксом `_id`.

| Имя | Соответствует | Замечания |
|-----|---------------|-----------|
| roles | да | множественное число |
| users | да | множественное число |
| products | да | множественное число |
| sizes | да | множественное число |
| stock_items | да | множественное число, snake_case |
| orders | да | множественное число |
| order_items | да | множественное число, snake_case |
| role_id | да | суффикс _id |
| role_name | да | snake_case |
| user_id | да | суффикс _id |
| last_name | да | snake_case |
| first_name | да | snake_case |
| middle_name | да | snake_case |
| login | да | - |
| product_id | да | суффикс _id |
| product_name | да | snake_case |
| category | да | - |
| manufacturer | да | - |
| price | да | - |
| image_path | да | snake_case |
| size_id | да | суффикс _id |
| size_value | да | snake_case |
| stock_item_id | да | суффикс _id |
| quantity | да | - |
| order_id | да | суффикс _id |
| order_date | да | snake_case |
| status | да | - |
| order_item_id | да | суффикс _id |