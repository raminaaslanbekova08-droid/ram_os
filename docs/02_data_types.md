 Типы данных для полей БД shoe_store

 Таблица roles

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| role_id | INTEGER | идентификатор роли | да | - | PRIMARY KEY AUTOINCREMENT |
| role_name | TEXT | название роли | да | - | UNIQUE |

 Таблица users

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| user_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| last_name | TEXT | фамилия | да | - | - |
| first_name | TEXT | имя | да | - | - |
| middle_name | TEXT | отчество | нет | NULL | - |
| login | TEXT | логин | да | - | UNIQUE |
| role_id | INTEGER | ссылка на роль | да | - | FOREIGN KEY → roles |

 Таблица products

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| product_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| product_name | TEXT | наименование | да | - | - |
| category | TEXT | категория | да | - | - |
| manufacturer | TEXT | производитель | да | - | - |
| price | NUMERIC(10,2) | цена | да | - | CHECK (price > 0) |
| image_path | TEXT | путь к изображению | нет | NULL | - |

 Таблица sizes

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| size_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| size_value | REAL | значение размера | да | - | UNIQUE |

 Таблица stock_items

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| stock_item_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| product_id | INTEGER | ссылка на товар | да | - | FOREIGN KEY → products |
| size_id | INTEGER | ссылка на размер | да | - | FOREIGN KEY → sizes |
| quantity | INTEGER | количество | да | 0 | CHECK (quantity >= 0) |

 Таблица orders

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| order_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | ссылка на пользователя | да | - | FOREIGN KEY → users ON DELETE RESTRICT |
| order_date | TEXT (ISO 8601) | дата заказа | да | CURRENT_DATE | - |
| status | TEXT | статус | да | 'new' | - |

 Таблица order_items

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|------|------------|------------|----------|---------|-------------|
| order_item_id | INTEGER | идентификатор | да | - | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | ссылка на заказ | да | - | FOREIGN KEY → orders ON DELETE CASCADE |
| stock_item_id | INTEGER | ссылка на товарную позицию | да | - | FOREIGN KEY → stock_items |
| quantity | INTEGER | количество | да | - | CHECK (quantity > 0) |
| price | NUMERIC(10,2) | цена позиции | да | - | CHECK (price > 0) |

