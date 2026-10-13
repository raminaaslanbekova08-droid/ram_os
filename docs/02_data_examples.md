 Примеры данных

 roles
| role_id | role_name |
|---------|-----------|
| 1 | admin |
| 2 | manager |
| 3 | user |

 users
| user_id | last_name | first_name | middle_name | login | role_id |
|---------|-----------|------------|-------------|-------|---------|
| 1 | Админов | Админ | NULL | admin | 1 |
| 2 | Менеджеров | Менеджер | NULL | manager | 2 |
| 3 | Пользователев | Пользователь | NULL | user | 3 |

 products
| product_id | product_name | category | manufacturer | price | image_path |
|------------|--------------|----------|--------------|-------|------------|
| 1 | Кроссовки Nike Air | спорт | Nike | 7990.00 | images/nike_air.jpg |
| 2 | Туфли Clarks | классика | Clarks | 12990.00 | images/clarks.jpg |
| 3 | Ботинки Timberland | повседневная | Timberland | 15990.00 | images/timberland.jpg |
| 4 | Сандалии Adidas | лето | Adidas | 3990.00 | images/adidas_sandals.jpg |
| 5 | Кеды Converse | спорт | Converse | 5490.00 | images/converse.jpg |

 sizes
| size_id | size_value |
|---------|------------|
| 1 | 36 |
| 2 | 37 |
| 3 | 38 |
| 4 | 39 |
| 5 | 40 |

 stock_items
| stock_item_id | product_id | size_id | quantity |
|---------------|------------|---------|----------|
| 1 | 1 | 4 | 10 |
| 2 | 1 | 5 | 5 |
| 3 | 2 | 3 | 7 |
| 4 | 2 | 4 | 3 |
| 5 | 3 | 5 | 2 |
| 6 | 4 | 1 | 15 |
| 7 | 4 | 2 | 8 |
| 8 | 5 | 3 | 12 |
| 9 | 5 | 4 | 6 |
| 10 | 5 | 5 | 4 |

 orders
| order_id | user_id | order_date | status |
|----------|---------|------------|--------|
| 1 | 1 | 2024-01-15 | completed |
| 2 | 2 | 2024-02-20 | processing |
| 3 | 3 | 2024-03-05 | new |

 order_items
| order_item_id | order_id | stock_item_id | quantity | price |
|---------------|----------|---------------|----------|-------|
| 1 | 1 | 1 | 1 | 7990.00 |
| 2 | 1 | 8 | 2 | 5490.00 |
| 3 | 2 | 3 | 1 | 12990.00 |
| 4 | 2 | 6 | 1 | 3990.00 |
| 5 | 3 | 5 | 1 | 15990.00 |
| 6 | 3 | 10 | 1 | 5490.00 |