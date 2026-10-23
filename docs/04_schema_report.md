 Отчёт о структуре БД shoe_store

 Порядок создания таблиц
1. roles
2. sizes
3. users        (FK -> roles)
4. products
5. stock_items  (FK -> products, sizes)
6. orders       (FK -> users)
7. order_items  (FK -> orders, stock_items)

Порядок отражает зависимости: сначала родительские таблицы, затем дочерние.

 Таблицы

 roles
- Поля: role_id (INTEGER PK AUTOINCREMENT), role_name (TEXT NOT NULL UNIQUE)
- Индексы: автоиндекс на role_name (UNIQUE)

 sizes
- Поля: size_id (INTEGER PK AUTOINCREMENT), size_value (REAL NOT NULL UNIQUE CHECK 20<v<50)
- Тип REAL, так как размеры бывают дробные (36.5)

 users
- Поля: user_id (PK), last_name, first_name (NOT NULL), middle_name (nullable),
  login (NOT NULL UNIQUE CHECK length 3..20), role_id (NOT NULL FK -> roles)
- FK: role_id -> roles(role_id) ON DELETE RESTRICT
- Индексы: idx_users_role_id

 products
- Поля: product_id (PK), category (NOT NULL), subcategory (nullable),
  manufacturer (NOT NULL), product_name (NOT NULL CHECK непустое),
  image_path, composition, description (nullable), price (REAL NOT NULL CHECK 0<price<1e6)
- Индексы: idx_products_category

 stock_items
- Поля: stock_item_id (PK), product_id (NOT NULL FK), size_id (NOT NULL FK),
  quantity_available (INTEGER NOT NULL DEFAULT 0 CHECK >= 0)
- FK: product_id -> products ON DELETE RESTRICT,
       size_id -> sizes ON DELETE RESTRICT
- Индексы: idx_stock_items_product, idx_stock_items_size
- Назначение: разрешает M:N между products и sizes

 orders
- Поля: order_id (PK), order_date (TEXT NOT NULL, ISO 8601),
  user_id (NOT NULL FK -> users)
- FK: user_id -> users ON DELETE RESTRICT
- Индексы: idx_orders_user_id, idx_orders_order_date

 order_items
- Поля: order_item_id (PK), order_id (NOT NULL FK), stock_item_id (NOT NULL FK),
  quantity (INTEGER NOT NULL CHECK > 0), price (REAL NOT NULL CHECK > 0)
- FK: order_id -> orders ON DELETE CASCADE,
       stock_item_id -> stock_items ON DELETE RESTRICT
- Индексы: idx_order_items_order, idx_order_items_stock